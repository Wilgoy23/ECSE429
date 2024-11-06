Feature: Filter Todo Items
  As a user
  I want to filter todo items based on different criteria
  So that I can easily find specific tasks

  Background:
    Given the following todo items exist:
      | id | title                    | doneStatus | description                        |
      | 1  | "Complete tax returns"   | true       | "Important"                        |
      | 2  | "Buy groceries"          | false      | "Get milk and eggs"                |
      | 3  | "Schedule dentist"       | true       | "Important"                        |
      | 4  | "Review presentation"    | false      | "Important"                        |
      | 5  | "Clean garage"           | true       | "Weekend cleaning"                 |

  Scenario: Successfully filter todo items by description (Normal Flow)
    When I send a GET request to "/todos?description=Important"
    Then the response status should be 200
    And the response body should contain 3 todo items
    And all todo items in response should contain description with "Important"

  Scenario: Successfully filter todo items by done status (Alternate Flow)
    When I send a GET request to "/todos?doneStatus=true"
    Then the response status should be 200
    And the response body should contain 3 todo items
    And all todo items in response should have "doneStatus" set to "true"

  Scenario: Attempt to filter todo items with an invalid field (Error Flow)
    When I send a GET request to "/todos?invalidField=value"
    Then the response status should be 400
    And the response body should contain an error message indicating "Invalid field name: invalidField"