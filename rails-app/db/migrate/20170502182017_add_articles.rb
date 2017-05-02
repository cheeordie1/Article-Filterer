class AddArticles < ActiveRecord::Migration[5.0]
  def change
    create_table :articles do |t|
      t.string     :text
      t.string     :authors
      t.string     :title
    end
  end
end
