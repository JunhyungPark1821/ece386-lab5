# Art Institute of Chicago API

Prompt engineering to have a LLM make a Python script to query exhibitions.

***Student**, Complete below.*

## Stats

### How many different prompts did you have to try before it worked?
- We tried two different prompts before it worked.

### How well did the final produced script work?
- The final produced script fulfilled all the tasks and goals that were listed. So, it worked successfully.

### What are some of the artwork titles from the exhibition "Ink on Paper: Japanese Monochromatic Prints (2009)"
- The Poetess Ukon, from the series The Thirty-six Immortal Women Poets (Nishikizuri onna sanjurokkasen)

## Prompt
I want you to complete a Python code for me. I will give you background information about the API, exhibitions endpoint, and a python template.

## Goals of the Code
1.	Accepts a search term from the user.
2.	Searches the ArtIC API for exhibitions matching that term and that have artwork titles.
3.	Prompts the user for a number of exhibitions they would like to view.
4.	Displays the titles of the artwork for those exhibition to the user.
5.	Loops until user exit.

## Search API Background
The Art Institute of Chicago (opens new window)'s API provides JSON-formatted data as a REST-style service that allows developers to explore and integrate the museum’s public data into their projects. This API is the same tool that powers our website (opens new window), our mobile app (opens new window), and many other technologies in the museum.

Behind the scenes, our search is powered by Elasticsearch (opens new window). You can use its Query DSL (opens new window)to interact with our API. The example above uses a term (opens new window)query. Other queries we use often include exists (opens new window)and bool (opens new window). Aggregations (opens new window)are also a powerful tool.

Our API accepts queries through both GET and POST. For production use, we recommend using GET and passing the entire query as minified URL-encoded JSON via the params parameter. 

### Conventions
•	We refer to models in our API as "resources" (e.g. artworks, artists, places)
•	Resources are typically accessed via their endpoints. Each resource has three endpoints:
o	Listing (e.g. /artworks)
o	Detail (e.g. /artworks/{id})
o	Search (e.g. /artworks/search) (optional)
Some resources might lack a search endpoint if there appears to be no need for it yet.
•	Multi-word endpoints are hyphenated (e.g. /tour-stop).
•	All field names are lowercase and snake case (underscore case).
•	Every resource in the API has id and title fields.
•	Fields that contain a single id reference to another resource are singular and end with _id:
•	"artist_id": 51349,
•	Fields that contain id references to multiple records from another resource are singular and end with _ids:
•	"style_ids": ["TM-4439", "TM-8542", "TM-4441"],
•	Fields that contain title references to records from other resources follow naming conventions similar to id-based fields:
•	"artist_title": "Ancient Roman",
•	"classification_titles": ["modern and contemporary art", "painting"],
•	Every title-based field has a keyword subfield in Elasticsearch, which is meant for filters and aggregations. See "New defaults" section in this article (opens new window)for more info.
•	Numeric and boolean fields get parsed into actual numbers and booleans:
•	"artwork_id": "45", // BAD
•	"date_start": 1942, // GOOD
•	
•	"is_preferred": "True", // BAD
•	"is_in_gallery": true, // GOOD
•	We never show any empty strings in the API. We only show null:
•	"date_display": "", // BAD
•	"artist_display": null, // GOOD
•	We prefer to always show all fields, even if they are null for the current record:
o	If a field that typically returns a string, number, or object is empty for a given record, we return it as null, rather than omitting it.
o	If a field typically returns an array, we prefer to return an empty array, rather than returning null. This is done in part for backwards-compatibility reasons.

## Best Practices
Here are some tips that will make your application run faster and/or reduce load on our systems:
•	Cache API responses in your system when possible.
•	Use the fields parameter to tell us exactly what fields you need.
•	Batch detail queries with the multi-id parameter (?ids=).
•	Batch search queries with multi-search (/msearch).
•	When downloading images, use /full/843,/0/default.jpg parameters.
•	When scraping, please use a single thread and self-throttle.
•	Consider using data dumps instead of scraping our API


## Exhibitions Endpoint
GET /exhibitions
A list of all exhibitions sorted by last updated date in descending order. For a description of all the fields included with this response, see here.
#Available parameters:
•	ids - A comma-separated list of resource ids to retrieve
•	limit - The number of resources to return per page
•	page - The page of resources to retrieve
•	fields - A comma-separated list of fields to return per resource
•	include - A comma-separated list of subresource to embed in the returned resources. Available options are:
o	artworks
o	sites
#Description of All Fields
•	id integer - Unique identifier of this resource. Taken from the source system.
•	api_model string - REST API resource type or endpoint
•	api_link string - REST API link for this resource
•	title string - The name of this resource
•	is_featured boolean - Is this exhibition currently featured on our website?
•	position number - Numering position represnting the order in which this exhibition is featured on the website
•	short_description string - Brief explanation of what this exhibition is
•	web_url string - URL to this exhibition on our website
•	image_url string - URL to the hero image from the website
•	status string - Whether the exhibition is open or closed
•	aic_start_at ISO 8601 date and time - Date the exhibition opened at the Art Institute of Chicago
•	aic_end_at ISO 8601 date and time - Date the exhibition closed at the Art Institute of Chicago
•	gallery_id number - Unique identifier of the gallery that mainly housed the exhibition
•	gallery_title string - The name of the gallery that mainly housed the exhibition
•	artwork_ids array - Unique identifiers of the artworks that were part of the exhibition
•	artwork_titles array - Names of the artworks that were part of the exhibition
•	artist_ids array - Unique identifiers of the artist agent records representing who was shown in the exhibition
•	site_ids array - Unique identifiers of the microsites this exhibition is a part of
•	image_id uuid - Unique identifier of the preferred image to use to represent this exhibition
•	alt_image_ids array - Unique identifiers of all non-preferred images of this exhibition.
•	document_ids array - Unique identifiers of assets that serve as documentation for this exhibition
•	suggest_autocomplete_boosted object - Internal field to power the /autocomplete endpoint. Do not use directly.
•	suggest_autocomplete_all object - Internal field to power the /autosuggest endpoint. Do not use directly.
•	source_updated_at ISO 8601 date and time - Date and time the resource was updated in the source system
•	updated_at ISO 8601 date and time - Date and time the record was updated in the aggregator database
•	timestamp ISO 8601 date and time - Date and time the record was updated in the aggregator search index

GET /exhibitions/search
Search exhibitions data in the aggregator.
#Available parameters:
•	q - Your search query
•	query - For complex queries, you can pass Elasticsearch domain syntax queries here
•	sort - Used in conjunction with query
•	from - Starting point of results. Pagination via Elasticsearch conventions
•	size - Number of results to return. Pagination via Elasticsearch conventions
•	facets - A comma-separated list of 'count' aggregation facets to include in the results.

GET /exhibitions/{id}
A single exhibition by the given identifier. {id} is the identifier from our collections management system.

## Python Template
-	Use Requests library
o	import requests
-	These are the functions that I think I will need based on the goal. Make sure to have a descriptive name, use type-hints in the parameters and return field, and have '''Block comments''' that state what the function should do.
o	get_search_term()
o	search_exhibitions(search_term)
o	display_exhibition_count(exhibitions)
o	get_exhibition_count()
o	get_exhibition_artwork(exhibition_id)
o	display_exhibition_artwork(exhibition, artwork_titles)
o	continue_program()
-	# TODO: main function that starts fresh every time and repeatedly prompts the user



### Share the conversation URL
https://claude.ai/share/34bcdfce-d1a5-43ba-b734-93f0d0b5532b
