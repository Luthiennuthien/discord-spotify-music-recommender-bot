
import discord

from discord.ext import commands

from dotenv import load_dotenv

import pandas as pd

import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
load_dotenv()
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


import os
from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
TOKEN = os.getenv("DISCORD_TOKEN")

from spotipy.oauth2 import SpotifyOAuth



import spotipy.util as util

SCOPE = 'playlist-modify-public playlist-modify-private playlist-read-collaborative ugc-image-upload'

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)
spBOT= spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='',
    client_secret='',
    redirect_uri='http://localhost:8888/callback',
    scope=SCOPE)
)








bot = commands.Bot(command_prefix='/', intents=intents)



@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(info='info')
async def info(ctx):

    embed = discord.Embed(title='Information!',color=discord.Color.teal(),description='**Brief Explanation For Each Command;**')
    embed.add_field(name='***•/search***',value='\nThis command is used to **search** spotify **artists**.\n**In order to use it** you must first type;\n\n  *******  **/search (and then the artistname)**\n*Example*: **/search MF DOOM**',inline=False)
    embed.add_field(name='***•/findtrack***',value='This command is used to **search** spotify **playlists**.\n**In order to use it** you must first type;\n\n ******* **/findtrack (and then the trackID)**\n*Example*: **/search 2QfW9GOU1prSjYPpC7cYpt**\n-->You can see the **ID** using the **spotify web browser**.')
    embed.add_field(name='***•/user***',value='This command is used to **get the user data** from spotify.\n**In order to use it** you must first type;\n\n ******* **/user (and then the userID)**\n*Example*: **/user aq65jc9cdy5id1ct2w6s00eay**\n-->You can see the **ID** using the **spotify web browser**.\n--> ***USE THIS FIRST FOR RECOMMEND AND DISPLAYSTAT TO WORK***',inline=False)
    embed.add_field(name='***•/displaystat***',value='This command is used to **view the entered user stats**.\n**In order to use it** you must type;\n\n ******* **/displaystat**\n',inline=False)
    embed.add_field(name='***•/recommend***',value='This command is used to **recommend songs based on the entered user**.\n**In order to use it** you must type;\n\n ******* **/recommend**\n',inline=False)
    embed.add_field(name='***Bot Creator;**',
                    value='This bot is created by **#luthiennuthien** on discord.',
                    inline=False)
    embed.set_thumbnail(url='https://media.tenor.com/g2q5VyGBJPcAAAAi/musica-music.gif')
    embed.set_footer(text=f'*{ctx.author.name} created this embed*')
    await ctx.send(embed=embed)




@bot.command(searchartist = 'search')

async def search(ctx ,*args):
    arg = ' '.join(args)
    results = sp.search(q=arg, limit=5)
    print(results)

    for idx, track in enumerate(results['tracks']['items']):
        album_name = track['album']['name']
        album_preview = track['preview_url']


        embed = discord.Embed(title="Listen the preview", description="Click the link below to listen:", color=0xFF0000, url=album_preview, )
        embed.add_field(name=track['name'], value=f"[Listen Here]({album_preview})" ,inline=True)
        embed.set_thumbnail(url=track['album']['images'][1]['url'])


        await ctx.send \
            (f"{idx + 1}. {track['name']} in {[album_name]} Album by {track['artists'][0]['name']} \nPreview:")
        await ctx.send(embed=embed)

@bot.command(findtrack = 'findtrack')
async def findtrack(ctx ,arg):



    playlist = sp.playlist(arg)





    embed = discord.Embed(title=playlist['name'], description=f"By: {playlist['owner']['display_name']}", color=0xFF0000 ,url=playlist['external_urls']['spotify'])
    print(playlist['external_urls']['spotify'])
    embed.add_field(name='Stats', value=f"Public: {playlist['public']}\nFollowers:{[playlist['followers']['total']]}\nTrack Count:{playlist['tracks']['total']}\n", inline=True)
    embed.set_thumbnail(url=playlist['images'][0]['url'])
    print(playlist)
    await ctx.send(embed=embed)


def genre(user_id):
    playlists = []
    results = sp.user_playlists(user_id)

    while results:
        if results and 'items' in results:
            playlists.extend(results['items'])
            if results['next']:
                results = sp.next(results)
            else:
                results = None
        else:
            print("Results is None or does not have 'items'")
            break
    return playlists


def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        if results and 'items' in results:
            tracks.extend(results['items'])
            if results['next']:
                results = sp.next(results)
            else:
                results = None
        else:
            print("Results is None or does not have 'items'")
            break

    return tracks










@bot.command(user='user')
async  def user(ctx,arg):
    global playlists
    playlists = genre(arg)
    print(playlists)
    print(arg)

    user = (sp.user(user=arg)) ['display_name']
    embed = discord.Embed(title='Please Wait <a:writingloading:1270811208420823074>', description='Gathering User Data Takes Some Time.',
                          color=discord.Color.brand_red() )
    embed.set_thumbnail(url=ctx.author.display_avatar)
    embed.add_field(name= f'Loading Steps To Find User:{user}',value='**Finding The User**       :‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ✅\n**Fetching Data**         : ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ 🟨\n**Creating Dataframe**     :‎ ‎ ‎ ‎❌\n**Finding Preferences**    : ‎ ‎ ❌\n**Finalizing Results**     : ‎ ‎ ‎ ‎ ‎ ‎ ‎ ❌')
    embed.set_footer(text=f"*{ctx.author.name} made this embed.*")
    print('a')
    load_embed = await ctx.send(embed=embed)

    all_songs = []
    # df = pd.DataFrame()
    i = 0

    for playlist in playlists:

        playlist_id = playlist['id']
        playlist_name = playlist['name']

        tracks = get_playlist_tracks(playlist_id)

        for item in tracks:

            track = item['track']

            def get_track_data(track_id):


                if sp.audio_features(track_id):
                    audio_features = sp.audio_features(track_id)
                    return audio_features[0]
                else:
                    print("Track not found or no features available.")

            if track is not None:

                features = get_track_data(track['id'])

                if track:


                    # track['artists'][0]['id']))
                    artist_id = track['artists'][0]['id']

                    artist_info = sp.artist(artist_id)
                    genremusic = artist_info['genres']
                    print(i)

                    i += 1

                    if not genre:
                        genre.append('None')

                    if i == 429:
                        break

                    song_data = {
                        'Playlist Name': playlist_name,
                        'Track Name': track['name'],
                        'Artist': ', '.join([artist['name'] for artist in track['artists']]),
                        'Genre': ',  '.join(genremusic),
                        'popularity': track['popularity'],
                        'Album': track['album']['name'],
                        'Release Date': track['album']['release_date'],
                        'Duration (ms)': track['duration_ms'],
                        'Danceability': features['danceability'],
                        'Energy': features['energy'],
                        'Loudness': features['loudness'],
                        'Speechiness': features['speechiness'],
                        'Acousticness': features['acousticness'],
                        'Instrumentalness': features['instrumentalness'],
                        'Tempo': features['tempo'],
                        'User': (sp.user(user=arg)) ['display_name']

                    }

                    all_songs.append(song_data)
                if i == 426:


                    break


        if i == 426:
            break

    embed.clear_fields()
    embed.add_field(name=f'Loading Steps To Find User:{user}',
                    value='**Finding The User**       :‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ✅\n**Fetching Data**         : ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ✅\n**Creating Dataframe**     :‎ ‎ ‎ ‎❌\n**Finding Preferences**    : ‎ ‎ ❌\n**Finalizing Results**     : ‎ ‎ ‎ ‎ ‎ ‎ ‎ ❌')


    df = pd.DataFrame(all_songs)
    df.to_csv(f'spotify_user_songs_{ctx.author}.csv', index=False)

    stats = pd.read_csv(f'spotify_user_songs_{ctx.author}.csv')

    await asyncio.sleep(5)


    embed.clear_fields()
    embed.add_field(name=f'Loading Steps To Find User:{user}',
                    value='**Finding The User**       :‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ✅\n**Fetching Data**         : ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ✅\n**Creating Dataframe**     :‎ ‎ ‎ ‎✅\n**Finding Preferences**    : ‎ ‎ ❌\n**Finalizing Results**     : ‎ ‎ ‎ ‎ ‎ ‎ ‎ ❌')
    await load_embed.edit(embed=embed)

    await asyncio.sleep(5)

    embed.clear_fields()
    embed.add_field(name=f'Loading Steps To Find User:{user}',
                    value='**Finding The User**       :‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ✅\n**Fetching Data**         : ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ✅\n**Creating Dataframe**     :‎ ‎ ‎ ‎✅\n**Finding Preferences**    : ‎ ‎ ✅\n**Finalizing Results**     : ‎ ‎ ‎ ‎ ‎ ‎ ‎ ❌')
    await load_embed.edit(embed=embed)
    await asyncio.sleep(2)

    embed = discord.Embed(title='DONE!!!', description='DONE!!!',
                          color=discord.Color.brand_green())
    embed.clear_fields()
    embed.add_field(name=f'DONE!!!!! User Data For {user} FOUND!',
                    value='**Finding The User**       :‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ✅\n**Fetching Data**         : ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ✅\n**Creating Dataframe**     :‎ ‎ ‎ ‎✅\n**Finding Preferences**    : ‎ ‎ ✅\n**Finalizing Results**     : ‎ ‎ ‎ ‎ ‎ ‎ ‎ ✅')
    embed.set_footer(text=f"*{ctx.author.name} made this embed.*")
    embed.set_thumbnail(url=ctx.author.display_avatar)
    await load_embed.edit(embed=embed)








songs = pd.read_csv('dataset.csv')




@bot.command(displaystat = 'displaystat')
async def displaystat(ctx):



    stats = pd.read_csv(f'spotify_user_songs_{ctx.author}.csv')
    USER = stats.loc[1]['User']
    print(USER)
    stats_popularity = (int((stats.get('popularity')).mean()))

    stats_danceability = (((stats.get('Danceability')).mean()))

    stats_energy = (((stats.get('Energy')).mean()))

    stats_loudness = (((stats.get('Loudness')).mean()))

    stats_speechiness = (((stats.get('Speechiness')).mean()))

    stats_acousticness = (((stats.get('Acousticness')).mean()))

    stats_instrumentalness = (((stats.get('Instrumentalness')).mean()))

    stats_tempo = (int((stats.get('Tempo')).mean()))

    genre_counts = stats['Genre'].value_counts()

    artist_counts = (stats['Artist']).value_counts()


    top_5_genre = list(((genre_counts).nlargest(5)).index)
    top_5_artists = list(((artist_counts).nlargest(5)).index)
    print(top_5_genre)
    new_top_5_genre = ', '.join(top_5_genre)
    new_top_5_artist = ', '.join(top_5_artists)
    print(new_top_5_artist)

    top_5_artists_count = ((artist_counts).nlargest(5)).to_string(index=True,header=False)

    individual_genres = [genre.strip() for genre in new_top_5_genre.split(' ')]



    def displayStatsINTEGER():
        return (
            f'Preferred Popularity: {stats_popularity}\nPreferred Danceability: {[stats_danceability]}\nPreferred Energy: {[stats_energy]}\nPreferred Loudness: {[stats_loudness]}\nPrefered Speechiness: {stats_speechiness}\nPreferred Acousticness: {stats_acousticness}\nPreferred Instrumentalness: {stats_instrumentalness}\nPreferred Tempo: {stats_tempo}')

    def displayStatsARTIST():
        return ([f'{top_5_artists_count}'])

    def displayStatsGENRE():
        return (f'{individual_genres}')

    embed = discord.Embed(title=f"{USER}'s Stats:", description=f'The stats {USER} looks for when listening to music:',
                          color=ctx.author.color, )
    embed.set_thumbnail(url=ctx.author.display_avatar)
    embed.set_footer(text=f"*{ctx.author.name} made this embed.*")
    embed.add_field(name=f"{USER}'s Preference In Every Stat;",
                    value=(displayStatsINTEGER()),
                    inline=True)
    embedArtist = discord.Embed(title=f"{USER}'s Favorite Artists;", description='The artists that reach out to you the most.',
                          color=ctx.author.color)
    embedArtist.set_thumbnail(url=ctx.author.display_avatar)
    embedArtist.add_field(name='Top 5 Artists;',
                    value=(f'\n{displayStatsARTIST()[0]}'),
                    inline=True)

    embedArtist.set_footer(text=f"*{ctx.author.name} made this embed.*")


    await ctx.send(embed=embed)

    await ctx.send(embed=embedArtist)









@bot.command(recommend='recommend')
async def recommend(ctx):
    def recommender():




        stats = pd.read_csv(f'spotify_user_songs_{ctx.author}.csv')
        USER = stats.loc[1]['User']
        stats_popularity = (int((stats.get('popularity')).mean()))

        stats_danceability = (((stats.get('Danceability')).mean()))

        stats_energy = (((stats.get('Energy')).mean()))

        stats_loudness = (((stats.get('Loudness')).mean()))

        stats_speechiness = (((stats.get('Speechiness')).mean()))

        stats_acousticness = (((stats.get('Acousticness')).mean()))

        stats_instrumentalness = (((stats.get('Instrumentalness')).mean()))

        stats_tempo = (int((stats.get('Tempo')).mean()))

        genre_counts = stats['Genre'].value_counts()

        artist_counts = (stats['Artist']).value_counts()


        top_5_genre = list(((genre_counts).nlargest(5)).index)
        new_top_5_genre = ', '.join(top_5_genre)
        top_5_artists = artist_counts.nlargest(5)
        individual_genres = [genre.strip() for genre in new_top_5_genre.split(' ')]

        filtered_df = songs[(songs['popularity'] >= stats_popularity - 20) & (
                    songs['popularity'] <= stats_popularity + 20 )]
        filtered_df = filtered_df[(filtered_df['tempo'] >= stats_tempo - 15) & (
                    filtered_df['tempo'] <= stats_tempo + 15)]
        filtered_df = filtered_df[(filtered_df['danceability'] >= stats_danceability - 0.3) & (
                    filtered_df['danceability'] <=stats_danceability + 0.2)]
        filtered_df = filtered_df[(filtered_df['energy'] >= stats_energy - 0.3) & (
                    filtered_df['energy'] <= stats_energy + 0.3)]
        filtered_df = filtered_df[(filtered_df['loudness'] >= stats_loudness - 6) & (
                    filtered_df['loudness'] <=stats_loudness + 6)]

        filtered_df = filtered_df[(filtered_df['acousticness'] >= stats_acousticness - 0.3) & (
                    filtered_df['acousticness'] <= stats_acousticness + 0.3)]
        filtered_df = filtered_df[(filtered_df['speechiness'] >= stats_speechiness - 0.2) & (
                    filtered_df['speechiness'] <= stats_speechiness + 0.2)]
        print(filtered_df['track_genre'])



        filtered_df = filtered_df[((filtered_df['track_genre']).isin(individual_genres))]


        print(filtered_df)

        print(individual_genres)
        print((filtered_df['track_genre']))

        print(filtered_df)
        filtered_df = filtered_df.sample(n=10)[['track_name','artists','track_id']]
        trackname = filtered_df[['track_name']]
        print(trackname)
        trackartists = filtered_df[['artists']]
        track_id = filtered_df[['track_id']]
        print(trackname)
        final = trackname.to_string(index=False, justify='center', header=False, col_space=6)
        finalartists = trackartists.to_string(index=False, justify='center', header=False, col_space=6)
        df = pd.DataFrame(data=track_id)
        df.to_csv(f'recommendations_{ctx.author}.csv', index=False)

        final_list = [final, finalartists,USER,track_id]

        return final_list

    recommendation = recommender()


    member = ctx.author.name

    print(ctx.author.color)

    embed = discord.Embed(title=F'Recommendations For {recommendation[2]}', description=f"**{recommendation[2]}'s Music Recommendations Based On Their Preferences** ",
                          color=ctx.author.color,type='rich')

    embed.add_field(name='Tracks',
                    value=(recommendation[0]),
                    inline=True)

    embed.add_field(name = 'Artists',value=(recommendation[1]),inline=True)


    embed.set_footer(text=f"*{member} made this embed.*")
    embed.set_thumbnail(url=ctx.author.display_avatar)



    await ctx.send(embed=embed)

@bot.command(personality='personality')
async def personality(ctx):
    try:
        stats = pd.read_csv(f'spotify_user_songs_{ctx.author}.csv')

        stats_popularity = (int((stats.get('popularity')).mean()))

        stats_danceability = (((stats.get('Danceability')).mean()))

        stats_energy = (((stats.get('Energy')).mean()))

        stats_loudness = (((stats.get('Loudness')).mean()))

        stats_speechiness = (((stats.get('Speechiness')).mean()))

        stats_acousticness = (((stats.get('Acousticness')).mean()))

        stats_instrumentalness = (((stats.get('Instrumentalness')).mean()))

        stats_tempo = (int((stats.get('Tempo')).mean()))

        genre_counts = stats['Genre'].value_counts()

        artist_counts = (stats['Artist']).value_counts()

        top_5_genre = list(((genre_counts).nlargest(5)).index)
        top_5_artists = list(((artist_counts).nlargest(5)).index)

        new_top_5_genre = ', '.join(top_5_genre)
        new_top_5_artist = ', '.join(top_5_artists)


        top_5_artists_count = ((artist_counts).nlargest(5)).to_string(index=True, header=False)

        individual_genres = [genre.strip() for genre in new_top_5_genre.split(' ')]

        def interpret_stat(value,stat_name):
            if value < 0.2:
                return f"very low {str(stat_name)}"
            elif value < 0.4:
                return f"low {str(stat_name)}"
            elif value < 0.6:
                return f"medium {str(stat_name)}"
            elif value < 0.8:
                return f"high {str(stat_name)}"
            else:
                return f"very high {str(stat_name)}"


            # return (
            #
            #     # f'Preferred Popularity: {stats_popularity}\nPreferred Danceability: {[stats_danceability]}\nPreferred Energy: {[stats_energy]}\nPreferred Loudness: {[stats_loudness]}\nPrefered Speechiness: {stats_speechiness}\nPreferred Acousticness: {stats_acousticness}\nPreferred Instrumentalness: {stats_instrumentalness}\nPreferred Tempo: {stats_tempo}')

        stats_popularitya = interpret_stat(stats_popularity, 'popularity')
        stats_danceabilitya = interpret_stat(stats_danceability, 'danceability')
        stats_energya = interpret_stat(stats_energy, 'energy')
        stats_loudnessa = interpret_stat(stats_loudness, 'loudness')
        stats_speechinessa = interpret_stat(stats_speechiness, 'speechiness')
        stats_acousticnessa = interpret_stat(stats_acousticness, 'acousticness')
        stats_instrumentalnessa = interpret_stat(stats_instrumentalness, 'instrumentalness')
        stats_tempoa = interpret_stat(stats_tempo, 'tempo')

        def displayStats():
             return(f'Preferred Popularity: {stats_popularitya}\nPreferred Danceability: {[stats_danceabilitya]}\nPreferred Energy: {[stats_energya]}\nPreferred Loudness: {[stats_loudnessa]}\nPrefered Speechiness: {stats_speechinessa}\nPreferred Acousticness: {stats_acousticnessa}\nPreferred Instrumentalness: {stats_instrumentalnessa}\nPreferred Tempo: {stats_tempoa}')


        def displayStatsARTIST():
            return ([f'{top_5_artists_count}'])

        def displayStatsGENRE():
            return (f'{individual_genres}')


        await ctx.send(displayStats())


    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command(create='create')
async def create(ctx):
    stats = pd.read_csv(f'spotify_user_songs_{ctx.author}.csv')
    USER = stats.loc[1]['User']
    ids = pd.read_csv(f'recommendations_{ctx.author}.csv')
    playlist = spBOT.user_playlist_create(user=f'31tpbhq3igbuid7k6bp5ryft27ke',name=f'Recommendations For {USER}',public=True,description=f'Recommendations')
    playlist_id = playlist['id']

    print(playlist_id)
    listIDS = []
    for index, row in ids.iterrows():
        track_id = row['track_id']
        print(track_id)

        listIDS.append(track_id)
    print(listIDS)

    spBOT.user_playlist_add_tracks(user='31tpbhq3igbuid7k6bp5ryft27ke', playlist_id=playlist_id, tracks=listIDS,position=None)
    spBOT.playlist_upload_cover_image(playlist_id=playlist_id,image_b64='data:image/png;base64,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')
    embed = discord.Embed(title=f'Playlist For {USER}.',
                          description='Enjoy listening to the recommended musics!',
                          color=discord.Color.brand_red(),url=playlist['external_urls']['spotify'])
    embed.set_thumbnail(url=ctx.author.display_avatar)
    embed.add_field(name=f'Mumender Hopes You Like It!',
                    value='Enjoy...')

    embed.set_footer(text=f"*{ctx.author.name} made this embed.*")
    print(playlist)
    await ctx.send(embed=embed)



bot.run(TOKEN)



