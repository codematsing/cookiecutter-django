# Test Plan

A test plan is a document that outlines the strategy, objectives, scope, and approach for testing a software application or system. It describes the overall testing process, including the test objectives, the types of tests to be performed, the testing environment, the testing resources needed, the testing schedule, and the roles and responsibilities of the testing team.

A test plan typically includes the following components:

* Introduction: Provides an overview of the software application or system being tested and outlines the purpose of the test plan.
* Test objectives: Defines the goals of the testing process, such as identifying defects, validating functionality, or measuring performance.
* Test scope: Specifies what will be tested, what will not be tested, and any dependencies or constraints that might affect the testing process.
* Test approach: Outlines the methodology and techniques that will be used to test the software, such as manual testing, automated testing, or a combination of both.
* Test environment: Describes the hardware, software, and other resources needed to conduct the testing process.
* Test schedule: Outlines the timelines and milestones for the testing process, including key dates and deadlines.
* Test deliverables: Specifies the documents, reports, and other materials that will be produced during the testing process.
* Test team: Describes the roles and responsibilities of the testing team members, including testers, developers, and stakeholders.

By creating a comprehensive test plan, the testing team can ensure that all aspects of the software application or system are thoroughly tested and that any issues or defects are identified and resolved before the software is released to the end-users.

Reference:
[Test Plan Template](https://www.tacticalprojectmanager.com/test-case-template-excel-with-example/)

|**Process**|**Test Case**|**Step**|**Description**|**Status**|**Expected Result**|**Actual Result**|**Comment**
| :- | :- |:- |:- |:- |:- |:- |:- |
| Login | Valid Credentials | 1 | Enter valid username and password | PASS | User is logged in | User is logged in | - |
| Login | Invalid Credentials | 1 | Enter invalid username and password | FAIL | Error message is displayed | Error message is displayed | - |
| Login | Empty Credentials | 1 | Leave both fields empty | FAIL | Error message is displayed | Error message is displayed | - |
| Signup | Valid Information | 1 | Enter valid user information | PASS | User is registered | User is registered | - |
| Signup | Invalid Email | 1 | Enter an invalid email address | FAIL | Error message is displayed | Error message is displayed | - |
| Signup | Password Mismatch | 1 | Enter two different passwords | FAIL | Error message is displayed | Error message is displayed | - |
| Profile | Edit Profile Picture | 1 | Click on "Edit Profile Picture" button | PASS | File explorer window opens | File explorer window opens | - |
| Profile | Edit Profile Information | 1 | Change some information and click "Save" | PASS | Information is updated | Information is updated | - |