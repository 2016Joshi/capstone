
import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor


CASTING_ASSISTANT = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjAzeEtha09Zdk8xa1A1Rk5naHRoYSJ9.eyJpc3MiOiJodHRwczovL2pvc2hpZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI2Y2M5Zjk3MTQwMzMwMDcwYjM0Njk2IiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE2NTYyNjQ3OTUsImV4cCI6MTY1NjI3MTk5NSwiYXpwIjoiclIzTzJCTDJsVGVUcFUxMkJ2NEhhZXZUNW1wWVNPb2oiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.ejSl_ufskQ6PMhex1UI8ttMpyuJYWmYPwBJr3GHMp2bu2bmU_wYMKiXtg27dtDs6BWK4eV8O8qLHwLSMzNhnbsqxhjlEoIF6nZcgo0UMGi3gGfva7vlA5A9qpwmP5K0XPL4Qvl-3Qp5xt9f1WDWrWV4kLIiIK2IiFV4kMnjnjfd_AUx71H-F-7pyQeZWDinXwSpnLGWuEG8ou_JY60lrNIYPPYPcZXItBC67eQ7jyWkCtsuqZL-4G2OH_iahibw0MDfzGi9C1wSyBY0YkfnUuJ90tTXsbGdgV6kU2ZfqATEaWmbXWVz1CgugYXCeg7fT-G5KYQq1HDeJEgRvfglGcQ')

CASTING_DIRECTOR = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjAzeEtha09Zdk8xa1A1Rk5naHRoYSJ9.eyJpc3MiOiJodHRwczovL2pvc2hpZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJiODViM2FlYTAyMzRhZTk3ZmVkZjczIiwiYXVkIjoiY2FzdGluZy1hZ2VuY3kiLCJpYXQiOjE2NTYyNzMyMzYsImV4cCI6MTY1NjI4MDQzNiwiYXpwIjoiclIzTzJCTDJsVGVUcFUxMkJ2NEhhZXZUNW1wWVNPb2oiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.nzWv3G5c6kM8ck-ATlO3a3IYJZWeW6KtUFSAF4z7WRUb-ByI0HO-x1-zoZmfMG95epk7bRYs_J4DUzy63d1KPgPAQUFpEKIr96yHFHzMLakY3FGhP42_-6ywgeXW64FAIPT0HqouTaRyQwsvlUCpbnJnl5DqzxolL7kLKLCPqHWU3tdJlHK0YLiC7ey4ixTE-75d1zcMMK2gAcZuY2_VotVALn1J6helQLz_zrjzHbhV4ImEbsFoSIU6UUm0XqhxUzBhraJ9hmXdXm7y1kR2iJOvhr9tMi5bu62Mts41r0ZoCK-203c9tgFJKyskIPK0KEJJmS5OLxJDko3o-VUqNg')

EXECUTIVE_PRODUCER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjAzeEtha09Zdk8xa1A1Rk5naHRoYSJ9.eyJpc3MiOiJodHRwczovL2pvc2hpZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDI5Mjg4MDg1MDkxOTI2ODMzMzYiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTY1NjI3NDA4NSwiZXhwIjoxNjU2MjgxMjg1LCJhenAiOiJyUjNPMkJMMmxUZVRwVTEyQnY0SGFldlQ1bXBZU09vaiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.vulOYTrmM3KiB76bgC0AVhJ4_lny7nPWEqCM05crms46FDWf-50ty2EzCGrBTdcS7mPubSzQN4BFxjvBMgzFqzkqHXVnagG2MjPZuzv1Til9DcFej-kTC70p-OmJ0YCKJzqvmug-vEu_QRw3bZcp2e6oSp0gHi7g78wTK9Arwv14UcOmc0BpoeVVItpkrGLKqdAWclIp_VZIr8bVxgzYH5cq_Sb7uPOX3tgTvITiBW3frpdOQ1ECXSZHeRCE7JxJVTht4e7vV3r0MSfa3sTh8Pm0UdTpaKB2A6TUcHdhmIYGWwcBrTsj3MQ0rj-xqwKZKA6HyFEBxcHgAd43s6h5DA')

class CastingAgencyTest(unittest.TestCase):
    """Test cases for Casting Agency"""
    # db_drop_and_create_all()
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.test_movie = {
            'title': 'Jurassic New',
            'release_date': '28/04/2022'
        }
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)
    
    def tearDown(self):
        pass

    """Get all movies"""
    def test_get_all_movies(self):
        response = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Test to get a specific movie
    def test_get_movie_by_id(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Jurassic')

     # tests for an invalid id to get a specific movie
    def test_404_get_movie_by_id(self):
        response = self.client().get(
            '/movies/404',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to create a movie
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Jurassic New')
        self.assertEqual(
            data['movie']['release_date'],
            'Wed, 27 Apr 2022 18:30:00 GMT'
        )


    # Test to create a movie without request body
    def test_400_post_movie(self):
        response = self.client().post(
            '/movies',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # Test to Update a movie
    def test_patch_movie(self):
        response = self.client().patch(
            '/movies/1',
            json={'title': 'Jurassic', 'release_date': "2022-06-27"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Jurassic')
        self.assertEqual(
            data['movie']['release_date'],
            'Sun, 26 Jun 2022 18:30:00 GMT'
        )
    
    # Test that 400 is returned if no data is sent to update a movie
    def test_400_patch_movie(self):
        response = self.client().patch(
            '/movies/1',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    
    #tests RBAC for creating a movie
    def test_401_post_movie_unauthorized(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    #tests RBAC for updating a movie
    def test_401_patch_movie_unauthorized(self):
        response = self.client().patch(
            '/movies/1',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests that 404 is returned for updating unavilable movie
    def test_404_patch_movie(self):
        response = self.client().patch(
            '/movies/12323',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # test to delete a movie
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/11',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # tests RBAC for deleting a movie
    def test_401_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


    # tests to delete a unavailable movie
    def test_404_delete_movie(self):
        response = self.client().delete(
            '/movies/1234',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    #  Tests to get all actors
    def test_get_all_actors(self):
        response = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Test to get a specific actor
    def test_get_actor_by_id(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'John')



    # tests for getting unavailable actor
    def test_404_get_actor_by_id(self):
        response = self.client().get(
            '/actors/10000',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to create an actor
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'John', 'age': 50, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'John')
        self.assertEqual(data['actor']['age'], 50)
        self.assertEqual(data['actor']['gender'], 'male')

    # Test to Update an actor
    def test_patch_actor(self):
        response = self.client().patch(
            '/actors/1',
            json={'name': 'Stuthi', 'age': 5, "gender": "female"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Stuthi')
        self.assertEqual(data['actor']['age'], 5)
        self.assertEqual(data['actor']['gender'], 'female')

    # Test that 400 is returned if no data is sent to update an actor
    def test_400_patch_actor(self):
        response = self.client().patch(
            '/actors/1',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # Test to verify 400 while creating an actor if no data is sent
    def test_400_post_actor(self):
        response = self.client().post(
            '/actors',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests RBAC for updating an actor by casting assistant
    def test_401_patch_actor_unauthorized(self):
        response = self.client().patch(
            '/actors/1',
            json={'name': 'John', 'age': 25, "gender": "male"},
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests that 404 is returned for an invalid id to get a specific actor
    def test_404_patch_actor(self):
        response = self.client().patch(
            '/actor/501',
            json={'name': 'Joshi', 'age': 35, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # test to delete an actor
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/2',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # tests RBAC for deleting an actor
    def test_401_delete_actor(self):
        response = self.client().delete(
            '/actors/5',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # test for deleting an invalid actor
    def test_404_delete_actor(self):
        response = self.client().delete(
            '/actors/1000',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

# Make the tests executable
if __name__ == "__main__":
    unittest.main()