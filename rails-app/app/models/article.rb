class Article < ActiveRecord::Base
    has_many :user_articles
    has_many :users, :through => :user_articles

    def getTitle
      return self.title
    end

    """ deprecated """
    def getParagraphs(user)
      http = Net::HTTP.new('nlp', 5001)
      request = Net::HTTP::Post.new('/highlight', {'Content-Type' => 'application/json'})
      data = {article_id: self.id, user_id: user.id}
      request.body = data.to_json
      response = http.request(request)
      highlighted = JSON.parse(response.body())
      return highlighted
    end

    def getHighlighted(user)
      http = Net::HTTP.new('nlp', 5001)
      request = Net::HTTP::Post.new('/highlight', {'Content-Type' => 'application/json'})
      data = {article_id: self.id, user_id: user.id}
      request.body = data.to_json
      response = http.request(request)
      article = JSON.parse(response.body())['article']
      return article
    end

end
