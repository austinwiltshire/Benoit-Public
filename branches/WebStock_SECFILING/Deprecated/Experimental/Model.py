from elixir import *

metadata.bind = "sqlite:///movies.sqlite"
metadata.bind.echo = True

class Genre(Entity):
	name = Field(Unicode(15), primary_key=True)
	movies = ManyToMany('Movie')

	def __repr__(self):
		return '<Genre "%s">' % self.name

class Movie(Entity):
    title = Field(Unicode(30), primary_key=True)
    year = Field(Integer, primary_key=True)
    description = Field(Unicode)
    director = ManyToOne('Director')
    genres = ManyToMany('Genre')
    
    def __repr__(self):
        return '<Movie "%s" (%d)>' % (self.title, self.year)

class Director(Entity):
	name = Field(Unicode(60))
	movies = OneToMany('Movie')

	def __repr__(self):
		return '<Director "%s">' % self.name
