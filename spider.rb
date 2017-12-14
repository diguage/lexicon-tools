require 'set'
require 'digest'
require 'rest-client'
require 'multi_json'

class Record
  attr_reader :rank, :word, :gender, :basic
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
     puts "#{@rank} === #{@word} === #{@gender}"
   end

   def toString
     "#{@rank}  #{@word}  #{@gender}"
   end
end

words = Set.new

appKey = '721dbf7775bc2936'
secKey = '2MRHAny83SDOzuoUuKUtiNleUdmbT3x6'
from = 'EN'
to = 'zh-CHS'
server = 'http://openapi.youdao.com/api'

# 签名，通过md5(appKey+q+salt+密钥)生成
def createSign(appKey, word, salt, secKey)
  Digest::MD5.hexdigest("#{appKey}#{word}#{salt}#{secKey}")
end

File.foreach('COCA20000.txt') do |line|
  r = Record.new(line)
  unless words.include?(r.word)
    words.add(r.word)
    fileName = "#{__dir__}/data/#{r.word}.json"

    next if File.exist? fileName

    puts r.display

    salt = Random.rand(1000)

    params = { q: r.word, from: from, to: to, appKey: appKey, salt: salt, sign: createSign(appKey, r.word, salt, secKey) }

    json = nil

    begin
      json = RestClient.get(server, {params: params}).to_s
    rescue RestClient::ExceptionWithResponse => e
      e.response
      sleep 600
      next
    end

    dict = MultiJson.load(json, :symbolize_keys => true)

    if dict[:errorCode] == "0"
      file = File.open(fileName, 'w')
      file.puts json
      file.close
    else
      sleep 600
    end
  end
end
