import wolframalpha
import wikipedia
import os



os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client-secret.json"
client = wolframalpha.Client('your-key')



import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "all-bot-yhniuh"



from gnewsclient import gnewsclient
nclient = gnewsclient.NewsClient(max_results=3)


from omdb import OMDBClient
mclient = OMDBClient(apikey="your-key")



from pymongo import MongoClient
mongo_client = MongoClient("mongodb+srv://vishav:vishav@cluster0-pju5e.mongodb.net/test?retryWrites=true&w=majority")
db = mongo_client.get_database('all_data')







def get_movie(parameters):
	mclient.topic = parameters.get('movie_name')
	return mclient.search_movie(mclient.topic)



def get_news(parameters):
    records = db.news_db
    new_news = {'Topic':parameters.get('news_type'),'Language':parameters.get('language'),'Location':parameters.get('geo-country')}
    nclient.topic = parameters.get('news_type')
    nclient.language = parameters.get('language')
    nclient.location = parameters.get('geo-country')
    records.insert_one(new_news)
    return nclient.get_news()



def get_info(parameters):
    search_bar = parameters.get('info')
    return search_bar







def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result




def removeHead(fromThis, removeThis):
    if fromThis.endswith(removeThis):
        fromThis = fromThis[:-len(removeThis)].strip()
    elif fromThis.startswith(removeThis):
        fromThis = fromThis[len(removeThis):].strip()
    return fromThis


def getReply(message, session_id):
    response = detect_intent_from_text(message, session_id)
    message = message.lower().strip()
    answer = ""
    



    
    if "wolfram" in message:
        message = removeHead(message, "wolfram")
        #try:
        answer = client.query(message)
        answer = next(answer.results).text
        #except:
         #   answer = "Request was not found using wolfram. Be more specific?"
    
    #elif "wiki" in message:
    elif response.intent.display_name == 'get_info':
        s = get_info(dict(response.parameters))
        message = removeHead(message, s)
        records = db.wiki_db
        records.insert_one({'Search':message})
        try:
            answer = wikipedia.summary(message)
        except:
            answer = "Request was not found using wiki. Be more specific?"


    elif response.intent.display_name == 'get_news':
        records = db.news_db
        news = get_news(dict(response.parameters))
        news_str = 'Here is your news: '
        for row in news:
            news_str += "\n\n{}\n\n{}\n\n".format(row['title'],row['link'])
        answer = news_str    
    
    elif response.intent.display_name == 'get_movie':
        records = db.movie_records
        news = get_movie(dict(response.parameters))
        news_str = 'Here is your movie:'
        news_str += "\n\n{}\n\n{}\n\n Year : {}\n\n".format(news[0].get('title'),news[0].get('poster'),news[0].get('year'))
        new_movie = {'Movie-Name':news[0].get('title'),'Year':news[0].get('year')}
        records.insert_one(new_movie)
    
        answer = news_str



    else:

        answer = "\n Welcome these are the command you can use like: \n wiki wiki-request\n wolfram your-request\n movies name request\n search any news "
    
    
    if len(answer) > 1500:
        answer = answer[0:1500] + "..."
    return answer
