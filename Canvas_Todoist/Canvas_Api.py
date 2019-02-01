import requests
import json

canvas_token = "5590~PBI1RLqkpw2nf7ybBYAfyYHEKPPN1Q5QAGaORQK2xGOZTCQ96qmx2YR4MeNu5POJ"


def target(query):
    url = 'https://canvas.instructure.com/api/v1/' + query + '?access_token=' + canvas_token
    r = requests.get(url)
    return r


course_list_raw = target("courses")
course_list = json.loads(course_list_raw.text)

# Canvas doesn't update which classes are active automatically.
# Need to individually select their location in course list.
active_course = [1, 2, 4, 5, 7]
course_ids = []
for i in active_course:
    course_ids.append(course_list[i]["id"])

# list assignments: /api/v1/courses/:course_id/assignments
all_assignments = []
for i in course_ids:
    i = str(i)
    assignment_location = "courses/" + i + "/assignments"
    all_assignments.append(json.loads(target(assignment_location).text))

# break down each class list into assignments and get name, due date, class id, and possible link to
# assignment(might not work because canvas for CWRU has different url
class_assignments = []
for i in range(len(all_assignments)):
    for j in range(len(all_assignments[i])):
        class_assignments.append(all_assignments[i][j])

for i in range(len(class_assignments)):
    for j in range(len(course_list)):
        if class_assignments[i]["course_id"] == course_list[j]["id"]:
            class_assignments[i]["course_name"] = course_list[j]["name"]
            print(class_assignments[i]["course_name"])
