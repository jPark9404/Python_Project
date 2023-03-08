from django.shortcuts import render
import googlemaps

# Create your views here.
def home(request):
    # gmaps = googlemaps.Client(key='AIzaSyC5csuoq6YNiXpBaDum9Xe9pxkvnYnSFUM')
    gmaps = googlemaps.Client(key='AIzaSyDW7ZBpXyfv9EfmspHb4PSZZMsKuSUHk3Q')

    place_name = 'Harmony Restaurant'
    places_result = gmaps.places(place_name)
    place_id = places_result['results'][0]['place_id']

    place = gmaps.place(place_id = place_id)
    reviews = []
    

    
    for i in range(len(place['result']['reviews'])):
        name = place['result']['reviews'][i]['author_name'] 
        date = place['result']['reviews'][i]['relative_time_description']
        rating = place['result']['reviews'][i]['rating']
        text = place['result']['reviews'][i]['text']
        img = place['result']['reviews'][i]['profile_photo_url']
        
        if int(rating)>=4:
            reviews.append({"Name": name,                                                
                            "Rating": rating,                        
                            "Date": date,                                                
                            "Text": text[0:195],
                            "Photo": img,
                            })
    

    context = {
        'reviews':reviews[0:3],
    }

    return render(request, 'home.html',context)


# def aboutUs(request):
#     return render(request, 'aboutUs_home.html', {})
    


   
