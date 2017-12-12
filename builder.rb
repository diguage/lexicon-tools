require 'set'
require 'digest'
require 'rest-client'
require 'multi_json'

class Record
  attr_reader :rank, :word, :gender
  attr_accessor :ukPhonetic, :usPhonetic, :meaning
  def initialize(line)
    line.strip!
    if (line =~ /^\d/).nil?
      @rank = 0
      @word = line
      @gender = nil
    else
      l = line.index(' ')
      r = line.rindex(' ')
      @rank = line[0..(l - 1)].strip.to_i
      @word = line[l..r].strip
      @gender = line[(r + 1)..-1].strip
    end
   end

   def display
     puts "rank: #{@rank} \nword: #{@word} \ngend: #{@gender} \nukPh: #{@ukPhonetic} \nusPh: #{@usPhonetic} \nmean: \n#{@meaning.join("\n")}"
   end

   def save(file)
    @ukPhonetic = '无' if @ukPhonetic.nil?
    @usPhonetic = '无' if @usPhonetic.nil?
    m = @meaning.join('</li><li>').gsub "\t", ' '
    separator = "@"
    file.puts "#{@word}　<sup>#{@rank}</sup>#{separator}#{@ukPhonetic}#{separator}#{@usPhonetic}#{separator}<ul><li>#{m}</li></ul>"
  end

   def toString
     "#{@rank}  #{@word}  #{@gender}"
   end
end

dictBasePath = "#{__dir__}/dictionaries"
mapDataFileName = "#{dictBasePath}/english-map-data.json"
mapData = {}
mapData =  MultiJson.load(IO.readlines(mapDataFileName)[0], :symbolize_keys => true) if File.exist? mapDataFileName


ankiDicFileName = "#{File.dirname(__FILE__)}/anki-coca-20000.txt"
# FileUtils.rm(ankiDicFileName) if File.exist? ankiDicFileName
ankiDicFile = File.new(ankiDicFileName, "w+")

dealedWord = Set.new 

# File.foreach('COCA20000.txt') do |line|
#   r = Record.new(line)
#   # break if r.rank > 10

#   next if dealedWord.include?(r.word)
#   dealedWord.add(r.word)
  
#   dictFileName = mapData[r.word.to_sym]
#   next unless File.exist? dictFileName

#   dict = MultiJson.load(IO.readlines(dictFileName)[0], :symbolize_keys => true)

#   # puts "\n================\n"
#   if !dict[:basic].nil?
#     r.ukPhonetic = dict[:basic][:'uk-phonetic']
#     r.usPhonetic = dict[:basic][:'us-phonetic']
#     r.meaning    = dict[:basic][:'explains']
#   elsif !dict[:web].nil?
#     r.meaning    = dict[:web][0][:value]
#   else
#     r.meaning    = dict[:translation]
#   end
#   # r.display
#   r.save(ankiDicFile)
# end

json = IO.readlines("#{__dir__}/coca20000-root.json").join(' ').gsub("\n", ' ')
wordList = MultiJson.load(json, :symbolize_keys => true)
# {"spelling":"I","introduction":"","rank":11,"gender":"p"},
wordList.each do |word|
  next if dealedWord.include?(word[:spelling].to_sym)
  dealedWord.add(word[:spelling].to_sym)
  dictFileName = "#{dictBasePath}/#{mapData[word[:spelling].to_sym]}"
  next unless File.exist? dictFileName

  dict = MultiJson.load(IO.readlines(dictFileName)[0], :symbolize_keys => true)

  # puts "\n================\n"
  ukPhonetic = nil
  usPhonetic = nil
  meaning = []

  if !dict[:basic].nil?
    ukPhonetic = dict[:basic][:'uk-phonetic']
    usPhonetic = dict[:basic][:'us-phonetic']
    meaning    = dict[:basic][:'explains']
  end
  unless dict[:web].nil?
    dict[:web].each { |w| meaning << "[Web](#{w[:key]})#{w[:value].join(';')}" } 
  end
  unless dict[:translation].nil?
    meaning << "[Tra]#{dict[:translation].join(';')}"
  end

  # r.display
  ukPhonetic = '无' if ukPhonetic.nil?
  usPhonetic = '无' if usPhonetic.nil?
  m = meaning.join('</li><li>').gsub "\t", ' '
  separator = "@"
  r = word[:root].nil? ? '无' : word[:root]

  ankiDicFile.puts "#{word[:spelling]}#{separator}#{ukPhonetic}#{separator}#{usPhonetic}#{separator}<ul><li>#{m}</li></ul>#{separator}#{r}#{separator}#{word[:rank]}"
end

ankiDicFile.close

puts "Build Anki Desk OK!"

