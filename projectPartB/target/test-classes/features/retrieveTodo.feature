Feature: Retrieve Todo Item
  As a user
  I want to retrieve todo items based on their id
  So that I can easily find specific tasks

  Background:
    Given the following todo item exists:
      | id  | title                        | doneStatus | description                |
      | "1" | "Complete project report"    | true       | "Need to finalize details" |

  Scenario: Normal Flow - Retrieve an existing todo item by ID
    When I send a GET request to "/todos/1"
    Then the response status should be 200
    And the response body should contain the todo item with the title "Complete project report"

  Scenario: Error Flow - Attempt to retrieve a todo item with a non-existing ID
    When I send a GET request to "/todos/999"
    Then the response status should be 404
    And the response body should contain an error message indicating "Could not find an instance with todos/999"

  Scenario: Alternate Flow - Attempt to retrieve a todo item without a valid ID
    When I send a GET request to "/todos/"
    Then the response status should be 404
