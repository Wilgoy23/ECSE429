Feature: Delete Todo Item
  As a user
  I want to be able to delete todo items
  So that I can keep order in the manager

  Background:
    Given the following todo items exist:
      | id | title           | doneStatus | description        |
      | 1  | "Buy groceries" | false      | "Get milk and eggs"|
      | 2  | "Pay bills"     | true       | "Utilities due"    |

  Scenario: Successfully delete an existing todo item (Normal Flow)
    When I send a DELETE request to "/todos/1"
    Then the response status should be 200
    When I send a GET request to "/todos/1"
    Then the response status should be 404
    And the response body should contain an error message indicating "Could not find an instance with todos/1"

  Scenario: Delete a todo item that was just deleted (Alternate Flow)
    Given I send a DELETE request to "/todos/1"
    When I send a DELETE request to "/todos/1"
    Then the response status should be 404
    And the response body should contain an error message indicating "Could not find an instance with todos/1"

  Scenario: Attempt to delete a todo item with invalid ID format (Error Flow)
    When I send a DELETE request to "/todos/999"
    Then the response status should be 404
    And the response body should contain an error message indicating "Could not find any instances with todos/999"