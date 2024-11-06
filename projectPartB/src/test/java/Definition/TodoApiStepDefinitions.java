package Definition;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.en.*;
import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;

import java.util.List;
import java.util.Map;


import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;


public class TodoApiStepDefinitions {
    private Response response;
    private String baseUri = "http://localhost:4567";
    private String jsonBody;



    @Before
    public void checkServiceAvailability() {
        // Perform a health check on the service before any tests
        Response healthCheckResponse = given()
                .contentType("application/json")
                .when()
                .get(baseUri + "/todos");

        assertEquals(200, healthCheckResponse.getStatusCode(), "Service is not running!");
    }

    @Before
    public void Initialize() {
        Response response = RestAssured.given()
                .accept(ContentType.JSON)
                .when()
                .get(baseUri + "/todos");

        if (response.statusCode() == 200) {
            // Parse response JSON to get the list of todo IDs
            List<String> todoIds = response.jsonPath().getList("todos.id", String.class); // Adjusted JSON path to access todo IDs

            // Step 2: Iterate over each todo ID and delete the todo
            for (String todoId : todoIds) {
                // Send DELETE request to delete each todo
                RestAssured.given()
                        .when()
                        .delete(baseUri + "/todos/" + todoId)
                        .then()
                        .statusCode(200); // Assert that deletion was successful
            }
        }
    }



    @Given("the following todo item:")
    public void givenTheFollowingTodoItem(io.cucumber.datatable.DataTable dataTable) {
        // You can parse the DataTable to extract values if needed
        // For this example, we will just store the jsonBody in the correct format
        jsonBody = dataTable.asLists().get(1).toString().replace("[", "{").replace("]", "}")
                .replace(", ", ",\"").replace("=", "\":").replace("[", "")
                .replace("]", "").replace("\"", "")
                .replace(":", "\":\"").replace(", ", "\",\"")
                .replace("}", "}");
    }

    @Given("the following todo item exists:")
    public void givenTheFollowingTodoItemExists(io.cucumber.datatable.DataTable dataTable) {
        // Extract the todo item details from the DataTable
        List<List<String>> data = dataTable.asLists(String.class); // Convert DataTable to a List of Lists
        String title = data.get(1).get(1).replace("\"", ""); // Get the title and remove extra quotes
        String doneStatus = data.get(1).get(2); // Get the done status
        String description = data.get(1).get(3).replace("\"", ""); // Get the description and remove extra quotes

        // Create the todo item JSON body
        String jsonBody = String.format(
                "{\"title\": \"%s\", \"doneStatus\": %s, \"description\": \"%s\"}",
                title, doneStatus.toLowerCase(), description); // Ensure doneStatus is lowercase for JSON boolean


        // Send POST request and capture the response
        Response response = given()
                .contentType("application/json")
                .body(jsonBody)
                .when()
                .post(baseUri + "/todos");

        // Assert that the response status code is 201 (Created)
        response.then().statusCode(201);
    }

    @Given("the following todo items exist:")
    public void givenTheFollowingTodoItemsExist(io.cucumber.datatable.DataTable dataTable) {
        List<Map<String, String>> todos = dataTable.asMaps(String.class, String.class);

        for (Map<String, String> todo : todos) {
            String title = todo.get("title").replace("\"", "");
            String description = todo.get("description").replace("\"", "");
            String doneStatus = todo.get("doneStatus");

            String jsonBody = String.format(
                    "{\"title\": \"%s\", \"doneStatus\": %s, \"description\": \"%s\"}",
                    title, doneStatus, description);

            Response response = given()
                    .contentType("application/json")
                    .body(jsonBody)
                    .when()
                    .post(baseUri + "/todos");

            response.then().statusCode(201);
        }
    }



    @When("I send a POST request to {string} with the following JSON:")
    public void whenISendAPostRequestToWithTheFollowingJson(String endpoint, String json) {
        response = given()
                .contentType("application/json")
                .body(json)
                .when()
                .post(baseUri + endpoint);
    }

    @When("I send a PUT request to {string} with the following JSON:")
    public void whenISendAPuttRequestToWithTheFollowingJson(String endpoint, String json) {
        response = given()
                .contentType("application/json")
                .body(json)
                .when()
                .put(baseUri + endpoint);
    }

    @When("I send a GET request to {string}")
    public void whenISendAGetRequestTo(String endpoint) {
        response = given()
                .contentType("application/json")
                .when()
                .get(baseUri + endpoint);
    }

    @When("I send a DELETE request to {string}")
    public void whenISendADeleteRequestTo(String endpoint) {
        response = given()
                .contentType("application/json")
                .when()
                .delete(baseUri + endpoint);
    }

    @Then("the response body should contain a todo item with {string} set to {string}")
    public void thenTheResponseBodyShouldContainATodoItemWithFieldSetTo(String field, String value) {
        // Convert string "true"/"false" to boolean if the field is doneStatus
        if (field.equals("doneStatus")) {
            response.then()
                    .body(field, equalTo(Boolean.parseBoolean(value)));
        } else {
            response.then()
                    .body(field, equalTo(value));
        }
    }

    @Then("the response body should contain the todo item with updated fields:")
    public void thenTheResponseBodyShouldContainTheTodoItemWithUpdatedFields(io.cucumber.datatable.DataTable dataTable) {
        List<Map<String, String>> data = dataTable.asMaps(String.class, String.class);
        Map<String, String> expectedFields = data.get(0);

        // For each field in the datatable, verify it matches in the response
        expectedFields.forEach((field, value) -> {
            // Remove quotes from the value if present
            String cleanValue = value.replace("\"", "");
            response.then()
                    .body(field, equalTo(cleanValue));
        });
    }

    @Then("the response body should contain the todo item with original title {string}")
    public void thenTheResponseBodyShouldContainTheTodoItemWithOriginalTitle(String title) {
        response.then()
                .body("title", equalTo(title.replace("\"", "")));
    }

    @Then("the response body should contain the todo item with description {string}")
    public void thenTheResponseBodyShouldContainTheTodoItemWithDescription(String description) {
        response.then()
                .body("description", equalTo(description.replace("\"", "")));
    }

    @Then("the response status should be {int}")
    public void thenTheResponseStatusShouldBe(int statusCode) {
        response.then().statusCode(statusCode);
    }

    @Then("the response body should contain the created todo item with the title {string}")
    public void thenTheResponseBodyShouldContainTheCreatedTodoItemWithTheTitle(String title) {
        response.then().body("title", equalTo(title));
    }

    @Then("the response body should contain the created todo item with the title {string} and an empty description")
    public void thenTheResponseBodyShouldContainTheCreatedTodoItemWithTheTitleAndAnEmptyDescription(String title) {
        response.then()
                .body("title", equalTo(title))
                .body("description", isEmptyOrNullString());
    }

    @Then("the response body should contain an error message indicating the title cannot be empty")
    public void thenTheResponseBodyShouldContainAnErrorMessageIndicatingTheTitleCannotBeEmpty() {
        response.then()
                .body("errorMessages", hasItem(containsString("Failed Validation: title : can not be empty"))); // Adjust to match the actual message
    }


    @Then("the response body should contain the todo item with the title {string}")
    public void thenTheResponseBodyShouldContainTheTodoItemWithTheTitle(String title) {
        response.then().body("todos[0].title", equalTo(title));
    }

    @Then("the response body should contain an error message indicating {string}")
    public void thenTheResponseBodyShouldContainAnErrorMessageIndicatingTheTodoItemWasNotFound(String arg) {
        response.then()
                .body("errorMessages", hasItem(containsString(arg))); // Adjust this to match the actual message
    }

    @Then("the response body should contain {int} todo items")
    public void theResponseBodyShouldContainNTodoItems(int expectedCount) {
        String responseBody = response.asString();
        System.out.println("Response Body: " + responseBody); // Print the response for debugging
        response.then()
                .body("todos.size()", equalTo(expectedCount));
    }

    @Then("all todo items in response should contain description with {string}")
    public void allTodoItemsInResponseShouldContainDescriptionWith(String descriptionText) {
        List<String> descriptions = response.jsonPath().getList("todos.description");

        for (String description : descriptions) {
            assertTrue(description.toLowerCase().contains(descriptionText.toLowerCase()),
                    "Description '" + description + "' does not contain '" + descriptionText + "'");
        }
    }

    @Then("all todo items in response should have {string} set to {string}")
    public void allTodoItemsInResponseShouldHaveFieldSetTo(String field, String value) {
        List<Object> fieldValues = response.jsonPath().getList("todos." + field);

        for (Object fieldValue : fieldValues) {
            if (field.equals("doneStatus")) {
                // Convert the expected value to boolean and compare with the string value from the response
                boolean expectedBooleanValue = Boolean.parseBoolean(value);
                String actualStringValue = fieldValue.toString(); // Get the actual value as string

                // Compare the expected boolean value with the actual string representation
                assertEquals(expectedBooleanValue, "true".equalsIgnoreCase(actualStringValue),
                        "Todo item has incorrect " + field + " value");
            } else {
                // Handle other fields as strings
                assertEquals(value, fieldValue.toString(),
                        "Todo item has incorrect " + field + " value");
            }
        }
    }

/*
    @After
    public void deleteAllTodos() {
        Response response = RestAssured.given()
                .accept(ContentType.JSON)
                .when()
                .get(baseUri + "/todos");


        if (response.statusCode() == 200) {
            // Parse response JSON to get the list of todo IDs
            List<String> todoIds = response.jsonPath().getList("todos.id", String.class); // Adjusted JSON path to access todo IDs


            // Step 2: Iterate over each todo ID and delete the todo
            for (String todoId : todoIds) {
                // Send DELETE request to delete each todo
                RestAssured.given()
                        .when()
                        .delete(baseUri + "/todos/" + todoId)
                        .then()
                        .statusCode(200); // Assert that deletion was successful
            }
        }
    }


 */

}

