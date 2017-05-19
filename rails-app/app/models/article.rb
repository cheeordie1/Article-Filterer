class Article < ActiveRecord::Base
    has_many :user_articles
    has_many :users, :through => :user_articles

    def getTitle
      return self.title
    end

    def getParagraphs
      return self.text
    end

end
