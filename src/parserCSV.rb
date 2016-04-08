# https://gist.github.com/callumj/1002363

class String
  def is_header?()
    return self.strip.match(/(===)(.+)(===)/)
  end
  
  def header()
    match_data = self.strip.match(/(===)(.+)(===)/)
    return match_data[2].strip
  end
  
  def percentage_value()
    match_data = self.strip.match(/([0-9.]+\s+%)/)
    if (match_data != nil && match_data.size >= 2)
      match_data[1].gsub(/\s%/, "%")
    else
      nil
    end
  end
  
  def number_value()
    match_data = self.strip.match(/([0-9]+.*[0-9]+)/)
    return match_data[1] if (match_data != nil && match_data.size >= 2)
    nil
  end
  
  def any_number()
    line_val = self.percentage_value
    line_val = self.number_value if line_val == nil
    
    if line_val != nil
      line_val
    else
      nil
    end
  end
end

def parse_file(file_path)
  results = []
  file_p = File.open(file_path)
  lines = file_p.readlines
  file_p.close

  prev_header = ""
  lines.each do |line|
    prev_header =  line.header if line.is_header?
  
    if prev_header.eql?("Summary")
      #puts line.strip unless line.strip.empty?
      results <<  line.any_number if line.any_number != nil
    elsif line.include?("Weighted Avg.")
      line.split(/\s+/).each do |val|
        results << val.any_number if val.any_number != nil
      end
    end
  end
  results
end

if (ARGV[0] == nil)
  $stderr.puts "Please specify a directory containing log files as the first argument"
else
  Dir["#{ARGV[0]}/*.txt"].each do |f|
    parsed_data = parse_file(f)
    if parsed_data.size >= 1
      line_str = "\"#{f}\","
      parsed_data.each do |value|
        line_str << value
        line_str << "," unless parsed_data.last == value
      end
      puts line_str
    end
  end
end