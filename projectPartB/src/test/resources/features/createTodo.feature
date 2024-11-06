Feature: Create Todo Item
  As a user
  I want to create todo items based on daily tasks
  So that I can easily manage tasks


  Background:
    Given the following todo item:
      | title                        | doneStatus | description                |
      | "Complete project report"   | true       | "Need to finalize details" |

  Scenario: Normal Flow - Create a new todo item
    When I send a POST request to "/todos" with the following JSON:
      """
      {
        "title": "Complete project report",
        "doneStatus": true,
        "description": "Need to finalize details"
      }
      """
    Then the response status should be 201
    And the response body should contain the created todo item with the title "Complete project report"

  Scenario: Alternate Flow - Create a todo item without a description
    When I send a POST request to "/todos" with the following JSON:
      """
      {
        "title": "Complete project report",
        "doneStatus": true
      }
      """
    Then the response status should be 201
    And the response body should contain the created todo item with the title "Complete project report" and an empty description

  Scenario: Error Flow - Attempt to create a todo item with an empty title
    When I send a POST request to "/todos" with the following JSON:
      """
      {
        "title": "",
        "doneStatus": true,
        "description": "Need to finalize details"
      }
      """
    Then the response status should be 400
    And the response body should contain an error message indicating the title cannot be empty
