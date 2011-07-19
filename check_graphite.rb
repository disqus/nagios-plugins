#!/usr/bin/env ruby

require 'cgi'
require 'csv'
require 'logger'
require 'net/http'
require 'optparse'

$log = Logger.new(STDOUT)
$log.level = Logger::ERROR
options = {}

optparse = OptionParser.new do |opts|
  opts.banner = "Usage: #{$0} [options]"

  options[:graphite_url] = 'http://localhost/'
  opts.on('-U', '--graphite-url [URL]',
          "Query Graphite on URL (default: #{options[:graphite_url]})") do |u|
    options[:graphite_url] = u
  end

  opts.on('-t', '--targets [TARGET1,TARGET2]', Array,
          'Show metrics for TARGET1, TARGET2') do |t|
    options[:targets] = t
  end

  opts.on('--from TIME', 'Set start time to TIME') do |t|
    options[:from] = t
  end

  options[:until] = 'now'
  opts.on('--until [TIME]',
          "Set end time to TIME (default: #{options[:until]})") do |t|
    options[:until] = t
  end

  opts.on('--percent [PCT]',
          'Set percent threshold to PCT') do |p|
    options[:percent] = p
  end

  opts.on('--threshold [VAL]',
          'set hard threshold to VAL') do |v|
    options[:threshold] = v
  end

  options[:over] = false
  opts.on('--over',
          'Alert on values over threshold (default: false)') do |o|
    options[:over] = true
  end

  opts.on('--under', 'Alert on values under threshold (default: true)') do |o|
    options[:under] = true
  end

  options[:warn_count] = 0
  opts.on('-W [NUM]',
          "Warn on NUM values beyond threshold (default: #{options[:warn_count]}") do |n|
    options[:warn_count] = n
  end

  options[:crit_count] = 0
  opts.on('-C [NUM]',
          "Critical on NUM values beyond threshold (default: #{options[:crit_count]}") do |n|
    options[:crit_count] = n
  end
end

begin
  optparse.parse!
  mandatory = [:targets, :from]
  missing = mandatory.select{ |param| options[param].nil? }
  if not missing.empty?
    puts "Missing options: #{missing.join(', ')}"
    puts optparse
    exit
  end

  mut_ex = [:percent, :threshold]
  if options[:percent] == true and options[:threshold] == true
    puts "--percent and --threshold are mutually exclusive."
    puts optparse
    exit
  end

  mut_ex = [:over, :under]
  if options[:over] == true and options[:under] == true
    puts "--over and --under are mutually exclusive."
    puts optparse
    exit
  end
rescue OptionParser::InvalidOption, OptionParser::MissingArgument
  puts $!.to_s
  puts optparse
  exit
end

class GraphiteFetcher
  def initialize(params)
    @graphite_url = params[:graphite_url].chomp('/')
    @targets = params[:targets].map {|t| "target=#{CGI::escape(t.to_s)}"}
    @from = CGI::escape(params[:from].to_s)
    @until = CGI::escape(params[:until].to_s)
  end

  def fetch_metrics
    metrics_by_col = []
    full_url = @graphite_url + '/render?' + [ @targets,
               "from=#{@from}",
               "until=#{@until}",
               "rawData=true"
    ].join('&')

    uri = URI.parse(full_url)
    $log.debug("Initiating HTTP request to url:#{full_url}")
    res = Net::HTTP.get_response(uri)

    res.value
    res.body.chomp.split("\n").each do |line|
      if line.include?('|')
        data = line.split('|')[1]
        idx = 0
        data.split(',').select {|x| x != 'None'}.each do |datum|
          metrics_by_col[idx] ||= 0
          metrics_by_col[idx] += datum.to_f
          idx += 1
        end
      end
    end

    raise "No data from graphite!" if metrics_by_col.empty? or metrics_by_col.nil?
    metrics_by_col
  end

  def check_threshold(data, block)
    beyond = []
    sorted = data.sort.map {|x| x.to_f}
    ceil = sorted[((sorted.length * 0.95).ceil)-1]
    sorted.each do |val|
      if block.call(val, ceil)
        beyond << val
      end
    end

    return ceil, beyond
  end
end

gs = GraphiteFetcher.new(:graphite_url => options[:graphite_url],
                         :targets => options[:targets],
                         :from => options[:from],
                         :until => options[:until])

if options[:over]
  block = Proc.new do |x, y|
    if options[:percent]
      result = x > y * options[:percent].to_i / 100.to_f
    else
      result = x > options[:threshold].to_i
    end

    result
  end
elsif options[:under]
  block = Proc.new do |x, y|
    if options[:percent]
      result = x < y * options[:percent].to_i / 100.to_f
    else
      result = x < options[:threshold].to_i
    end

    result
  end
end

begin
  metrics = gs.fetch_metrics
  ceil, alerting = gs.check_threshold(metrics, block)
rescue => e
  puts "CRITICAL: Caught exception: #{e.message}"
  exit 2
end

if alerting.length > 0
  if alerting.length >= options[:crit_count].to_i
    puts "CRITICAL: #{alerting.length} data point(s) alerting! (#{alerting.join(', ')})"
    exit 2
  elsif alerting.length >= options[:warn_count].to_i
    puts "WARNING: #{alerting.length} data point(s) alerting! (#{alerting.join(', ')})"
    exit 1
  else
    puts "OK: No data point(s) alerting."
  end
else
  puts "OK: No data point(s) alerting."
end
