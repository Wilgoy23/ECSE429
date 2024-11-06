Feature: Todo Content Update Operations
  As a user
  I want to update todo item details
  So that I can modify task information as needed

  Background:
    Given the following todo item exists:
      | id | title              | doneStatus | description          |
      | 1  | "Complete report"  | false      | "Q4 sales analysis" |

  Scenario: Successfully update a todo item's title and description (Normal Flow)
    When I send a PUT request to "/todos/1" with the following JSON:
      """
      {
        "title": "Finish Q4 report",
        "description": "Complete Q4 sales and revenue analysis",
        "doneStatus": false
      }
      """
    Then the response status should be 200
    And the response body should contain the todo item with updated fields:
      | title              | description                           |
      | "Finish Q4 report" | "Complete Q4 sales and revenue analysis" |

  Scenario: Update only the description of a todo item (Alternate Flow)
    When I send a PUT request to "/todos/1" with the following JSON:
      """
      {
        "description": "Updated Q4 sales analysis with new data"
      }
      """
    Then the response status should be 200
    And the response body should contain the todo item with original title "Complete report"
    And the response body should contain the todo item with description "Updated Q4 sales analysis with new data"

  Scenario: Attempt to update a todo item with empty title (Error Flow)
    When I send a PUT request to "/todos/1" with the following JSON:
      """
      {
        "title": ""
      }
      """
    Then the response status should be 400
    And the response body should contain an error message indicating "Failed Validation: title : can not be empty"
