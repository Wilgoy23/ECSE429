# Name: William Goyens  ID: 261120027  email: william.goyens@mail.mcgill.ca

import unittest
import requests
import json
import xml.etree.ElementTree as ET


BASE_URL = "http://localhost:4567"

class TodosAPITestCase(unittest.TestCase):
    # Set up initial system state
    def setUp(self):
        self.session = requests.Session()
        
        # Check if the API is running before proceeding
        try:
            response = self.session.get(f"{BASE_URL}")
            # If the API isn't returning 200, fail the setup
            self.assertEqual(response.status_code, 200)
        except requests.ConnectionError:
            self.session.close()
            self.fail()

        # Get the initial state of todos
        self.initial_todos = self.get_all_todos()
    
    # reset System State
    def tearDown(self):
        self.delete_all_todos()
        for todo in self.initial_todos:
            self.create_todo(todo)
        self.session.close()
    
    def get_all_todos(self):
        response = self.session.get(f"{BASE_URL}/todos")
        return response.json()
    
    
    def delete_all_todos(self):
        todos = self.get_all_todos()
        todo_ids = [todo['id'] for todo in todos['todos']]
        for ID in todo_ids:
            self.session.delete(f"{BASE_URL}/todos/{ID}")

    def create_todo(self, todo_data):
        return self.session.post(f"{BASE_URL}/todos", json=todo_data)

    # GET /todos
    def test_get_all_todos(self):
        response = self.session.get(f"{BASE_URL}/todos")
        self.assertEqual(response.status_code, 200)
        todos = response.json()
        self.assertIsInstance(todos, dict)

    # HEAD /todos
    def test_head_todos(self):
        response = self.session.head(f"{BASE_URL}/todos")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Type', response.headers)

    # POST /todos
    def test_create_todo(self):
        new_todo = {
            "title": "New Todo",
            "description": "This is a new todo",
            "doneStatus": False
        }
        response = self.create_todo(new_todo)
        self.assertEqual(response.status_code, 201)
        created_todo = response.json()
        self.assertIsNotNone(created_todo['id'])
        self.assertEqual(created_todo['title'], new_todo['title'])
        
    # PUT /todos (undocumented)
    def test_put_todo(self):
        new_todo = {
            "title": "New Todo",
            "description": "This is a new todo",
            "doneStatus": False
        }
        response = self.session.put(f"{BASE_URL}/todos")
        self.assertEqual(response.status_code, 405)
        
    # DELETE /todos (undocumented)
    def test_delete_todo(self):
        new_todo = {
            "title": "New Todo",
            "description": "This is a new todo",
            "doneStatus": False
        }
        response = self.session.delete(f"{BASE_URL}/todos")
        self.assertEqual(response.status_code, 405)
    
    # OPTIONS /todos (undocumented)
    def test_expected_options_todo(self):
        new_todo = {
            "title": "New Todo",
            "description": "This is a new todo",
            "doneStatus": False
        }
        response = self.session.options(f"{BASE_URL}/todos")
        self.assertNotEqual(response.status_code, 405)
        
    # OPTIONS /todos (Same for all other API endpoints... options is allowed to run undocumented) (undocumented)
    def test_observed_options_todo(self):
        new_todo = {
            "title": "New Todo",
            "description": "This is a new todo",
            "doneStatus": False
        }
        response = self.session.options(f"{BASE_URL}/todos")
        self.assertEqual(response.status_code, 200)
        
    # OPTIONS /todos
    def test_patch_todo(self):
        new_todo = {
            "title": "New Todo",
            "description": "This is a new todo",
            "doneStatus": False
        }
        response = self.session.patch(f"{BASE_URL}/todos")
        self.assertEqual(response.status_code, 405)

    # GET /todos/:id
    def test_get_specific_todo(self):
        new_todo = {"title": "Specific Todo", "description": "Get this specific todo"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        response = self.session.get(f"{BASE_URL}/todos/{todo_id}")
        self.assertEqual(response.status_code, 200)
        todo = response.json()['todos']
        self.assertEqual(todo[0]['id'], todo_id)
        self.assertEqual(todo[0]['title'], new_todo['title'])

    # HEAD /todos/:id
    def test_head_specific_todo(self):
        new_todo = {"title": "Head Todo", "description": "Head this specific todo"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        response = self.session.head(f"{BASE_URL}/todos/{todo_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Type', response.headers)

    # POST /todos/:id (amend)
    def test_amend_todo_post(self):
        new_todo = {"title": "Todo to Amend", "description": "This will be amended"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        amended_data = {"title": "Amended Todo"}
        response = self.session.post(f"{BASE_URL}/todos/{todo_id}", json=amended_data)
        self.assertEqual(response.status_code, 200)
        amended_todo = response.json()
        self.assertEqual(amended_todo['title'], amended_data['title'])

    # PUT /todos/:id
    def test_update_todo_put(self):
        new_todo = {"title": "Todo to Update", "description": "This will be updated"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        updated_data = {"title": "Updated Todo", "doneStatus": True}
        response = self.session.put(f"{BASE_URL}/todos/{todo_id}", json=updated_data)
        self.assertEqual(response.status_code, 200)
        updated_todo = response.json()
        self.assertEqual(updated_todo['title'], updated_data['title'])
        self.assertEqual(updated_todo['doneStatus'], str(updated_data['doneStatus']).lower())

    # DELETE /todos/:id
    def test_delete_todo(self):
        new_todo = {"title": "Todo to Delete", "description": "This will be deleted"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        response = self.session.delete(f"{BASE_URL}/todos/{todo_id}")
        self.assertEqual(response.status_code, 200)

        get_response = self.session.get(f"{BASE_URL}/todos/{todo_id}")
        self.assertEqual(get_response.status_code, 404)
        
    # PATCH /todos/:id (undocumented)
    def test_patch_specific_todo(self):
        new_todo = {"title": "Todo to Amend", "description": "This will be amended"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        amended_data = {"title": "Amended Todo"}
        response = self.session.patch(f"{BASE_URL}/todos/{todo_id}", json=amended_data)
        self.assertEqual(response.status_code, 405)
        
    # GET /todos/:id/tasksof
    def test_get_todo_tasksof(self):
        new_todo = {"title": "Todo with Tasks", "description": "This todo has tasks"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        response = self.session.get(f"{BASE_URL}/todos/{todo_id}/tasksof")
        self.assertEqual(response.status_code, 200)
        tasks = response.json()
        self.assertIsInstance(tasks, dict)

    # HEAD /todos/:id/tasksof
    def test_head_todo_tasksof(self):
        new_todo = {"title": "Todo with Tasks", "description": "This todo has tasks"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        response = self.session.head(f"{BASE_URL}/todos/{todo_id}/tasksof")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Type', response.headers)

    # POST /todos/:id/tasksof
    def test_create_todo_tasksof(self):
        new_todo = {"title": "Todo for Task Creation", "description": "This todo will have a task"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        # Assuming we have a project ID to relate to. In a real scenario, you'd create a project first.
        project_id = "1"
        response = self.session.post(f"{BASE_URL}/todos/{todo_id}/tasksof", json={"id": project_id})
        self.assertEqual(response.status_code, 201)
        
    # PUT /todos/:id/tasksof (undocumented)
    def test_create_todo_tasksof(self):
        new_todo = {"title": "Todo for Task Creation", "description": "This todo will have a task"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        # Assuming we have a project ID to relate to. In a real scenario, you'd create a project first.
        project_id = "1"
        response = self.session.post(f"{BASE_URL}/todos/{todo_id}/tasksof", json={"id": project_id})
        self.assertEqual(response.status_code, 201)

    # DELETE /todos/:id/tasksof/:id
    def test_delete_todo_tasksof_id(self):
        new_todo = {"title": "Todo for Task Deletion", "description": "This todo will have a task deleted"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        project_id = "1"
        self.session.post(f"{BASE_URL}/todos/{todo_id}/tasksof", json={"id": project_id})
        response = self.session.delete(f"{BASE_URL}/todos/{todo_id}/tasksof/{project_id}")
        self.assertEqual(response.status_code, 200)
        
        # checks that the created todo no longer has a task
        response = self.session.get(f"{BASE_URL}/todos/{todo_id}")
        self.assertRaises(KeyError, lambda: response.json()['todos'][0]['tasksof'])
       

    # GET /todos/:id/tasksof/:id (Expected Error 405)
    def test_get_todo_tasksof_id(self):
        new_todo = {"title": "Todo for Task Deletion", "description": "This todo will have a task deleted"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        project_id = "1"
        response = self.session.get(f"{BASE_URL}/todos/{todo_id}/tasksof/{project_id}")
        self.assertNotEqual(response.status_code, 405)
        
    def test_get_todo_tasksof_id_observed(self):
        new_todo = {"title": "Todo for Task Deletion", "description": "This todo will have a task deleted"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        project_id = "1"
        response = self.session.get(f"{BASE_URL}/todos/{todo_id}/tasksof/{project_id}")
        self.assertEqual(response.status_code, 404)

    # GET /todos/:id/categories
    def test_get_todo_categories(self):
        new_todo = {"title": "Todo with Categories", "description": "This todo has categories"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        response = self.session.get(f"{BASE_URL}/todos/{todo_id}/categories")
        self.assertEqual(response.status_code, 200)
        categories = response.json()
        self.assertIsInstance(categories, dict)

    # HEAD /todos/:id/categories
    def test_head_todo_categories(self):
        new_todo = {"title": "Todo with Categories", "description": "This todo has categories"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        response = self.session.head(f"{BASE_URL}/todos/{todo_id}/categories")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Content-Type', response.headers)

    # POST /todos/:id/categories
    def test_create_todo_category(self):
        new_todo = {"title": "Todo for Category Creation", "description": "This todo will have a category"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        # Assuming we have a category ID to relate to. In a real scenario, you'd create a category first.
        category_id = "1"
        response = self.session.post(f"{BASE_URL}/todos/{todo_id}/categories", json={"id": category_id})
        self.assertEqual(response.status_code, 201)

    # DELETE /todos/:id/categories/:id
    def test_delete_todo_category(self):
        new_todo = {"title": "Todo for Category Deletion", "description": "This todo will have a category deleted"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        category_id = "1"
        self.session.post(f"{BASE_URL}/todos/{todo_id}/categories", json={"id": category_id})
        response = self.session.delete(f"{BASE_URL}/todos/{todo_id}/categories/{category_id}")
        self.assertEqual(response.status_code, 200)

    def test_filter_todos(self):
        todo1 = {"title": "Done Todo", "doneStatus": True}
        todo2 = {"title": "Not Done Todo", "doneStatus": False}
        self.create_todo(todo1)
        self.create_todo(todo2)

        response = self.session.get(f"{BASE_URL}/todos?doneStatus=true")
        self.assertEqual(response.status_code, 200)
        todos = response.json()
        self.assertIsInstance(todos, dict)
        self.assertTrue(all(todo['doneStatus'] == 'true' for todo in todos['todos']))

    def test_xml_support(self):
        headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}
        xml_data = '''
        <todo>
            <title>XML Todo</title>
            <description>This is an XML todo</description>
            <doneStatus>false</doneStatus>
        </todo>
        '''
        response = self.session.post(f"{BASE_URL}/todos", data=xml_data, headers=headers)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.headers['Content-Type'], 'application/xml')
        
        root = ET.fromstring(response.content)
        self.assertEqual(root.find('title').text, 'XML Todo')
        self.assertEqual(root.find('description').text, 'This is an XML todo')
        self.assertEqual(root.find('doneStatus').text, 'false')

    def test_unexpected_side_effects(self):
        new_todo = {"title": "Test Todo", "description": "Description"}
        create_response = self.create_todo(new_todo)
        todo_id = create_response.json()['id']

        todos_before = self.get_all_todos()

        updated_data = {"title": "Updated Todo"}
        self.session.put(f"{BASE_URL}/todos/{todo_id}", json=updated_data)

        todos_after = self.get_all_todos()

        self.assertEqual(len(todos_before), len(todos_after))
        for before, after in zip(todos_before['todos'], todos_after['todos']):
            if before['id'] == todo_id:
                self.assertNotEqual(before['title'], after['title'])
            else:
                self.assertEqual(before, after)

if __name__ == '__main__':
    unittest.main()
    
    '''suite = unittest.TestSuite()
    suite.addTest(TodosAPITestCase('test_get_all_todos'))

    # Use a TextTestRunner to run the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)'''