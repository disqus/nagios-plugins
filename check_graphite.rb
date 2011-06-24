#!/usr/bin/env ruby
#                               Apache License
#                         Version 2.0, January 2004
#                      http://www.apache.org/licenses/
#
# TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
#
# 1. Definitions.
#
#    "License" shall mean the terms and conditions for use, reproduction,
#    and distribution as defined by Sections 1 through 9 of this document.
#
#    "Licensor" shall mean the copyright owner or entity authorized by
#    the copyright owner that is granting the License.
#
#    "Legal Entity" shall mean the union of the acting entity and all
#    other entities that control, are controlled by, or are under common
#    control with that entity. For the purposes of this definition,
#    "control" means (i) the power, direct or indirect, to cause the
#    direction or management of such entity, whether by contract or
#    otherwise, or (ii) ownership of fifty percent (50%) or more of the
#    outstanding shares, or (iii) beneficial ownership of such entity.
#
#    "You" (or "Your") shall mean an individual or Legal Entity
#    exercising permissions granted by this License.
#
#    "Source" form shall mean the preferred form for making modifications,
#    including but not limited to software source code, documentation
#    source, and configuration files.
#
#    "Object" form shall mean any form resulting from mechanical
#    transformation or translation of a Source form, including but
#    not limited to compiled object code, generated documentation,
#    and conversions to other media types.
#
#    "Work" shall mean the work of authorship, whether in Source or
#    Object form, made available under the License, as indicated by a
#    copyright notice that is included in or attached to the work
#    (an example is provided in the Appendix below).
#
#    "Derivative Works" shall mean any work, whether in Source or Object
#    form, that is based on (or derived from) the Work and for which the
#    editorial revisions, annotations, elaborations, or other modifications
#    represent, as a whole, an original work of authorship. For the purposes
#    of this License, Derivative Works shall not include works that remain
#    separable from, or merely link (or bind by name) to the interfaces of,
#    the Work and Derivative Works thereof.
#
#    "Contribution" shall mean any work of authorship, including
#    the original version of the Work and any modifications or additions
#    to that Work or Derivative Works thereof, that is intentionally
#    submitted to Licensor for inclusion in the Work by the copyright owner
#    or by an individual or Legal Entity authorized to submit on behalf of
#    the copyright owner. For the purposes of this definition, "submitted"
#    means any form of electronic, verbal, or written communication sent
#    to the Licensor or its representatives, including but not limited to
#    communication on electronic mailing lists, source code control systems,
#    and issue tracking systems that are managed by, or on behalf of, the
#    Licensor for the purpose of discussing and improving the Work, but
#    excluding communication that is conspicuously marked or otherwise
#    designated in writing by the copyright owner as "Not a Contribution."
#
#    "Contributor" shall mean Licensor and any individual or Legal Entity
#    on behalf of whom a Contribution has been received by Licensor and
#    subsequently incorporated within the Work.
#
# 2. Grant of Copyright License. Subject to the terms and conditions of
#    this License, each Contributor hereby grants to You a perpetual,
#    worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#    copyright license to reproduce, prepare Derivative Works of,
#    publicly display, publicly perform, sublicense, and distribute the
#    Work and such Derivative Works in Source or Object form.
#
# 3. Grant of Patent License. Subject to the terms and conditions of
#    this License, each Contributor hereby grants to You a perpetual,
#    worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#    (except as stated in this section) patent license to make, have made,
#    use, offer to sell, sell, import, and otherwise transfer the Work,
#    where such license applies only to those patent claims licensable
#    by such Contributor that are necessarily infringed by their
#    Contribution(s) alone or by combination of their Contribution(s)
#    with the Work to which such Contribution(s) was submitted. If You
#    institute patent litigation against any entity (including a
#    cross-claim or counterclaim in a lawsuit) alleging that the Work
#    or a Contribution incorporated within the Work constitutes direct
#    or contributory patent infringement, then any patent licenses
#    granted to You under this License for that Work shall terminate
#    as of the date such litigation is filed.
#
# 4. Redistribution. You may reproduce and distribute copies of the
#    Work or Derivative Works thereof in any medium, with or without
#    modifications, and in Source or Object form, provided that You
#    meet the following conditions:
#
#    (a) You must give any other recipients of the Work or
#        Derivative Works a copy of this License; and
#
#    (b) You must cause any modified files to carry prominent notices
#        stating that You changed the files; and
#
#    (c) You must retain, in the Source form of any Derivative Works
#        that You distribute, all copyright, patent, trademark, and
#        attribution notices from the Source form of the Work,
#        excluding those notices that do not pertain to any part of
#        the Derivative Works; and
#
#    (d) If the Work includes a "NOTICE" text file as part of its
#        distribution, then any Derivative Works that You distribute must
#        include a readable copy of the attribution notices contained
#        within such NOTICE file, excluding those notices that do not
#        pertain to any part of the Derivative Works, in at least one
#        of the following places: within a NOTICE text file distributed
#        as part of the Derivative Works; within the Source form or
#        documentation, if provided along with the Derivative Works; or,
#        within a display generated by the Derivative Works, if and
#        wherever such third-party notices normally appear. The contents
#        of the NOTICE file are for informational purposes only and
#        do not modify the License. You may add Your own attribution
#        notices within Derivative Works that You distribute, alongside
#        or as an addendum to the NOTICE text from the Work, provided
#        that such additional attribution notices cannot be construed
#        as modifying the License.
#
#    You may add Your own copyright statement to Your modifications and
#    may provide additional or different license terms and conditions
#    for use, reproduction, or distribution of Your modifications, or
#    for any such Derivative Works as a whole, provided Your use,
#    reproduction, and distribution of the Work otherwise complies with
#    the conditions stated in this License.
#
# 5. Submission of Contributions. Unless You explicitly state otherwise,
#    any Contribution intentionally submitted for inclusion in the Work
#    by You to the Licensor shall be under the terms and conditions of
#    this License, without any additional terms or conditions.
#    Notwithstanding the above, nothing herein shall supersede or modify
#    the terms of any separate license agreement you may have executed
#    with Licensor regarding such Contributions.
#
# 6. Trademarks. This License does not grant permission to use the trade
#    names, trademarks, service marks, or product names of the Licensor,
#    except as required for reasonable and customary use in describing the
#    origin of the Work and reproducing the content of the NOTICE file.
#
# 7. Disclaimer of Warranty. Unless required by applicable law or
#    agreed to in writing, Licensor provides the Work (and each
#    Contributor provides its Contributions) on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#    implied, including, without limitation, any warranties or conditions
#    of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
#    PARTICULAR PURPOSE. You are solely responsible for determining the
#    appropriateness of using or redistributing the Work and assume any
#    risks associated with Your exercise of permissions under this License.
#
# 8. Limitation of Liability. In no event and under no legal theory,
#    whether in tort (including negligence), contract, or otherwise,
#    unless required by applicable law (such as deliberate and grossly
#    negligent acts) or agreed to in writing, shall any Contributor be
#    liable to You for damages, including any direct, indirect, special,
#    incidental, or consequential damages of any character arising as a
#    result of this License or out of the use or inability to use the
#    Work (including but not limited to damages for loss of goodwill,
#    work stoppage, computer failure or malfunction, or any and all
#    other commercial damages or losses), even if such Contributor
#    has been advised of the possibility of such damages.
#
# 9. Accepting Warranty or Additional Liability. While redistributing
#    the Work or Derivative Works thereof, You may choose to offer,
#    and charge a fee for, acceptance of support, warranty, indemnity,
#    or other liability obligations and/or rights consistent with this
#    License. However, in accepting such obligations, You may act only
#    on Your own behalf and on Your sole responsibility, not on behalf
#    of any other Contributor, and only if You agree to indemnify,
#    defend, and hold each Contributor harmless for any liability
#    incurred by, or claims asserted against, such Contributor by reason
#    of your accepting any such warranty or additional liability.
#
# END OF TERMS AND CONDITIONS
#
# APPENDIX: How to apply the Apache License to your work.
#
#    To apply the Apache License to your work, attach the following
#    boilerplate notice, with the fields enclosed by brackets "[]"
#    replaced with your own identifying information. (Don't include
#    the brackets!)  The text should be enclosed in the appropriate
#    comment syntax for the file format. We also recommend that a
#    file or class name and description of purpose be included on the
#    same "printed page" as the copyright notice for easier
#    identification within third-party archives.
#
# Copyright 2011 DISQUS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

    begin
      uri = URI.parse(full_url)
      $log.debug("Initiating HTTP request to url:#{full_url}")
      res = Net::HTTP.get_response(uri)
    rescue => e
      $log.fatal("Caught exception: #{e.message}")
    end

    res.body.chomp.split("\n").each do |line|
      data = line.split('|')[1]
      idx = 0
      data.split(',').select {|x| x != 'None'}.each do |datum|
        metrics_by_col[idx] ||= 0
        metrics_by_col[idx] += datum.to_f
        idx += 1
      end
    end

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

class Integer
  def to_pct
    self.to_i / 100.to_f
  end
end

gs = GraphiteFetcher.new(:graphite_url => options[:graphite_url],
                         :targets => options[:targets],
                         :from => options[:from],
                         :until => options[:until])

metrics = gs.fetch_metrics

if options[:over]
  block = Proc.new do |x, y|
    if options[:percent]
      result = x > y * options[:percent].to_i.to_pct
    else
      result = x > options[:threshold].to_i
    end

    result
  end
elsif options[:under]
  block = Proc.new do |x, y|
    if options[:percent]
      result = x < y * options[:percent].to_i.to_pct
    else
      result = x < options[:threshold].to_i
    end

    result
  end
end

ceil, alerting = gs.check_threshold(metrics, block)

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
