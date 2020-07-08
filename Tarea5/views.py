from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context 
import requests
from Tarea5.settings import BASE_DIR

url_api = "https://integracion-rick-morty-api.herokuapp.com/graphql"

def homepage(request): #la barra buscadora y todos los capitulos con ciertos datos (son link buttons)

    query = """
            query {
                episodes {
                    results {
                        name
                        air_date
                        episode
                    }
                }
                }
            """

    response = requests.post(url_api, json={'query': query}).json() 
  #  print(response)
    episodes = response['data']['episodes']['results']

    home_template = open(BASE_DIR + "/Tarea5/Templates/home_temp.html")

    plt = Template(home_template.read())

    home_template.close()

    ctx = Context({"list_episodes": episodes, "total_episodes": len(episodes)}) 

    doc = plt.render(ctx)


    return HttpResponse(doc)

def episode(request, name_ep): #sin id, url ni creación
    query = """
            query {
                episodes (filter: {name: "%s"}) {
                    results {
                        name
                        air_date
                        episode
                        characters {
                            name
                        }
                    }
                }
            }
            """ % name_ep
    
    response = requests.post(url_api, json={'query': query}).json() 
    print("response", response)
    info_episode = response['data']['episodes']['results'][0]
    

    name = info_episode['name']
    air_date = info_episode['air_date']
    episode = info_episode['episode']
    characters = info_episode['characters'] 


    episode_template = open(BASE_DIR + "/Tarea5/Templates/episode_temp.html")

    plt = Template(episode_template.read())

    episode_template.close()

    ctx = Context({"name": name, "air_date": air_date, "episode": episode, "characters": characters})

    doc = plt.render(ctx)

    return HttpResponse(doc)

def character(request, name_ch): #sin id, url ni creación. Con todos sus lugares y episodios

    query = """
            query {
                characters (filter: {name: "%s"}) {
                    results {
                        name
                        status
                        species
                        type
                        gender
                        origin {
                            name
                        }
                        location {
                            name
                        }
                        image
                        episode {
                            name
                            episode
                        }
                    }
                }
            }

            """ % name_ch
    response = requests.post(url_api, json={'query': query}).json()
    print(response)
    info_character = response['data']['characters']['results'][0]
    name = info_character["name"]
    status = info_character["status"]
    species = info_character["species"]
    ch_type = info_character["type"]
    gender = info_character["gender"]
    origin = info_character["origin"]
    location = info_character["location"]
    image = info_character["image"]  #url
    list_episodes = info_character["episode"]  #lista con los url de cada episodio
   
   # last_location =  requests.get(location['url']).json()

 #   if origin['url'] != "":
  #      origin_location = requests.get(origin['url']).json()
   # else:
    #    origin_location = "Es un lugar con name unkwown"

 #   list_episodes = []
 #   for ele in episode:
  #      response = requests.get(ele).json()
   #     list_episodes.append(response)


    character_template = open(BASE_DIR + "/Tarea5/Templates/character_temp.html")

    plt = Template(character_template.read())

    character_template.close()

    ctx = Context({"name": name, "status": status, "species": species, "ch_type": ch_type, "gender": gender, "origin": origin,
    "location": location, "image": image, "episodes": list_episodes}) 

    doc = plt.render(ctx)

    return HttpResponse(doc)

def location(request, name_loc):

    query = """
            query {
                locations (filter: {name: "%s"}) {
                    results {
                        name
                        type
                        dimension
                        residents {
                            name
                        }
                    }
                }
            }
            """ % name_loc

    response = requests.post(url_api, json={'query': query}).json()
    print(response)
    info_locations = response['data']['locations']['results'][0]
    name = info_locations["name"]
    loc_type = info_locations["type"]
    dimension = info_locations["dimension"]
    residents = info_locations["residents"]

 #   list_residents = []
  #  for ele in residents:
   #     response = requests.get(ele).json()
    #    list_residents.append(response)

    location_template = open(BASE_DIR + "/Tarea5/Templates/location_temp.html")

    plt = Template(location_template.read())

    location_template.close()

    ctx = Context({"name": name, "loc_type": loc_type, "dimension": dimension, "residents": residents}) 

    doc = plt.render(ctx)

    return HttpResponse(doc)
    
def search(request): #iterar sobre las pages
    query = request.GET["query_input"]
    results_episodes = []
    results_characters = []
    results_locations = []
    query_ep = """
                query {
                    episodes (filter: {name: "%s"}) {
                        results {
                            name
                            air_date
                            episode
                            characters {
                                name
                            }
                        }
                    }
                }
            """ % query
    response_episodes = requests.post(url_api, json={'query': query_ep}).json()
    if "errors" not in response_episodes.keys():
        results_episodes = response_episodes['data']['episodes']['results']
        print('SEARCH EPISODES', results_episodes)

    query_ch = """
            query {
                characters (filter: {name: "%s"}) {
                    results {
                        name
                        status
                        species
                        type
                        gender
                        origin {
                            name
                        }
                        location {
                            name
                        }
                        image
                        episode {
                            name
                            episode
                        }
                    }
                }
            }

            """ % query
    response_characters = requests.post(url_api, json={'query': query_ch}).json()
    if "errors" not in response_characters.keys():
        results_characters = response_characters['data']['characters']['results']
        print('SEARCH CHARACTERS', results_characters)

    query_loc = """
                query {
                    locations (filter: {name: "%s"}) {
                        results {
                            name
                            type
                            dimension
                            residents {
                                name
                            }
                        }
                    }
                }
                """ % query
    response_locations = requests.post(url_api, json={'query': query_loc }).json()
    if "errors" not in response_locations.keys():
        results_locations = response_locations['data']['locations']['results']
        print('SEARCH LOCATIONS', results_locations)

    search_template = open(BASE_DIR + "/Tarea5/Templates/search_temp.html")

    plt = Template(search_template.read())

    search_template.close()

    ctx = Context({"query": query, "episodes": results_episodes, "characters": results_characters, "locations": results_locations}) 

    doc = plt.render(ctx)

    return HttpResponse(doc)

    