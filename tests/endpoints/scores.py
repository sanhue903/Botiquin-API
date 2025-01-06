import pytest
from tests import generate_session_data


def generate_json(chapter):
    request = generate_session_data(chapter)
    request['date'] = request['date'].strftime('%d-%m-%Y')
    request['chapter_id'] = chapter.id
    
    return request    

def make_headers(token):
  return {'Authorization': f'Bearer {token}'}

def count_scores(json):
    total = 0
    for session in json:
        total+= len(session["scores"])
    return total
    
def test_post_scores(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]
    
  request = generate_json(chapter)

  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores/', headers=headers, json=request)
    
  print(response.get_data())
  assert response.status_code == 201

def test_post_scores_wrong_app(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]

  request = generate_json(chapter)
    
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/WRONAP/students/{mock_student[0].id}/scores/', headers=headers, json=request)
    
  assert response.status_code == 404

def test_post_scores_no_authentication(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]
    
  request = generate_json(chapter)
    
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores/', json=request)
    
  assert response.status_code == 401
  
def test_post_scores_no_authorized(test_client, mock_app_content, mock_student, mock_user):
  chapter = mock_app_content['app'].chapters[0]
    
  request = generate_json(chapter)
      
  headers = {'Authorization': f'Bearer {mock_user["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores/', headers=headers, json=request)
    
  assert response.status_code == 403

def test_post_scores_wrong_student(test_client, mock_app_content):
  chapter = mock_app_content['app'].chapters[0]
  
  request = generate_json(chapter)
    
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/99/scores/', headers=headers, json=request)
  
  assert response.status_code == 404
  
def test_post_scores_wrong_chapter(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]
 
  request = generate_json(chapter)
  request['chapter_id'] = "WRONCH"
  
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores/', headers=headers, json=request)
  
  assert response.status_code == 404
  
def test_post_scores_wrong_question(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]

  request = generate_json(chapter)
  request['chapter_id'] = mock_app_content['app'].chapters[1].id

  print(request)
  
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores/', headers=headers, json=request)
  
  assert response.status_code == 404
  
def test_post_scores_missing_data(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]

  request = generate_json(chapter)
  request.pop('chapter_id')

 
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores/', headers=headers, json=request)
  
  assert response.status_code == 422

def test_post_scores_invalid_data(test_client, mock_app_content, mock_student):
  chapter = mock_app_content['app'].chapters[0]
  
  request = generate_session_data(chapter)
  request['chapter_id'] = chapter.id
  request['seconds'] = 'a'
  
  headers = {'Authorization': f'Bearer {mock_app_content["token"]}'}
  response = test_client.post(f'/apps/{mock_app_content["app"].id}/students/{mock_student[0].id}/scores/', headers=headers, json=request)
  
  assert response.status_code == 422
  
def test_get_scores(test_client, mock_user, mock_scores):
  headers = {'Authorization': f'Bearer {mock_user["token"]}'}
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores/', headers=headers)
  
  print(response.get_data())
  
  assert response.status_code == 200

 
  json = response.get_json()
  print(json)
  total_scores = count_scores(json)
  
  len_test_scores = 0
  for session in mock_scores[1]:
      len_test_scores+= len(session.scores)
      
  assert total_scores == len_test_scores

def test_get_scores_wrong_app(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user["token"])
  
  response = test_client.get('/apps/WROGAP/students/scores/', headers=headers)

  assert response.status_code == 404

def test_get_scores_no_authentication(test_client, mock_scores):
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores/')

  assert response.status_code == 401

def test_get_scores_no_authorized(test_client, mock_user, mock_application, mock_scores):
  headers = make_headers(mock_scores[0]['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores/', headers=headers)

  assert response.status_code == 403
  
def test_chapter_filter(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores/?chapter=TESCH1', headers=headers)
  
  assert response.status_code == 200
  
  json = response.get_json()
  
  len_test_scores = 0
  for session in mock_scores[1]:
      if session.chapter_id == 'TESCH1':
          len_test_scores+= len(session.scores)
  
  total_scores = count_scores(json)

  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores/?chapter=1', headers=headers)
      
  assert total_scores == len_test_scores

def test_wrong_chapter_filter(test_client, mock_user, mock_scores):
  headers = make_headers(mock_user['token'])
  
  response = test_client.get(f'/apps/{mock_scores[0]["app"].id}/students/scores/?chapter=WRONCH', headers=headers)
  
  json = response.get_json()
  
  assert len(json) == 0