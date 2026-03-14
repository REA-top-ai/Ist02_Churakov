rate_movie=lambda rating:'фильм понравился' if rating > 8.5 else 'Этот фильм был так себе'
print(rate_movie(9.6))
print(rate_movie(3))