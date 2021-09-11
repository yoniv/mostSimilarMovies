
#  get all genres on the movie requested with the list of movies that has the same genre
def get_same_genre(mydb, title):
    cursor = mydb.connection.cursor()
    sql = ("select CONCAT(title_list, title_list2, title_list3, title_list4) from movis.genremovies\
                    where (title_list like %s \
                    and title_list != %s) \
                    or (title_list2 like %s \
                    and title_list2 != %s)\
                    or (title_list3 like %s \
                    and title_list3 != %s)\
                    or (title_list4 like %s \
                    and title_list4 != %s)")
    like_val = '%' + title + '%'
    cursor.execute(sql, (like_val, title, like_val, title, like_val, title, like_val, title))

    same_genre = {}
    for row in cursor.fetchall():
        for title_movie in row[0].split(", "):
            if title_movie == title or title_movie == ' ':
                continue
            if title_movie in same_genre.keys():
                same_genre[title_movie] += 1
            else:
                same_genre[title_movie] = 1
    cursor.close()

    return same_genre
    

# get the count of similar key_words between the given title and all movies
def get_similar_words(mydb, title):
    cursor = mydb.connection.cursor()
    sql = ("select title_list from movis.wordassociation\
                    where title_list like %s \
                    and title_list != %s")
    like_val = '%' + title + '%'
    cursor.execute(sql, (like_val, title))

    same_word = {}
    for row in cursor.fetchall():
        for title_movie in row[0].split(","):
            if title_movie == title or title_movie == ' ':
                continue
            if title_movie in same_word.keys():
                same_word[title_movie] += 1
            else:
                same_word[title_movie] = 1
    cursor.close()
    return same_word


# get the most three similar movies by the closest genre and word from the plot_summary
def get_three_most_similar(same_genre, count_of_similar_words):
    most_similar = []
    three_most_similar = []
    max_genre_similar = {}
    max_lev = 0
    max_array = ['max1', 'max2', 'max3']
    if same_genre:
        most_similar = sorted(same_genre.items(), key=lambda x: x[1], reverse=True)
        max_sim_genre = most_similar[0][1]
        # if there are 3 movies with the same genre so they are the most similar
        if len(most_similar) == 3:
            for i in most_similar:
                three_most_similar.append(most_similar[i][0])
            return three_most_similar
        # if there are more than 3 we need to prioritize by the most similar keywords in the plot summary
        if len(most_similar) > 3:
            for movie in most_similar:
                if movie[1] == max_sim_genre:
                    if max_array[max_lev] in max_genre_similar:
                        max_genre_similar[max_array[max_lev]].append(movie[0])
                    else:
                        max_genre_similar[max_array[max_lev]] = [movie[0]]
                    continue

                if movie[1] < max_sim_genre:
                    if max_lev >= 2 or len(max_genre_similar[max_array[max_lev]]) >= 3:
                        break
                    max_lev += 1
                    max_genre_similar[max_array[max_lev]] = [movie[0]]
                    max_sim_genre = movie[1]
    # insert the 3 most similare by genre and most prioritize 
    if len(max_genre_similar) > 0:  
        need_to_add = 2 - max_lev
        similar_word_and_genre = {}
        for movies_level in max_genre_similar:
            mov = max_genre_similar[movies_level]
            if len(mov) <= need_to_add:
                for movie in mov:
                    three_most_similar.append(movie)
            else:
                for movie in mov:
                    if movie in count_of_similar_words:
                        similar_word_and_genre[movie] = count_of_similar_words[movie]
                    else:
                        similar_word_and_genre[movie] = 0

        most_similar_words = sorted(similar_word_and_genre.items(), key=lambda x: x[1], reverse=True)
        for i in most_similar_words:
            if len(three_most_similar) >= 3: 
                break
            three_most_similar.append(i[0])

    # if there are no similar genres then we take from the most similar words 
    if len(most_similar) == 0:
        most_similar = sorted(count_of_similar_words.items(), key=lambda x: x[1], reverse=True)
        for i in most_similar:
            if len(three_most_similar) >= 3:
                break
            three_most_similar.append(i[0])
    
    return three_most_similar

        




    


            


