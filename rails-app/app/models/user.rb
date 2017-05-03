

class User < ApplicationRecord
  has_many :user_articles
  has_many :articles, :through => :user_articles

  class << self
    def from_omniauth(auth_hash)
      user = find_or_create_by(uid: auth_hash['uid'], provider: auth_hash['provider'])
      user.name = auth_hash['info']['name']
      user.location = auth_hash['info']['location']
      user.image_url = auth_hash['info']['image']
      user.save!
      user
    end
  end

end
