import requests
import json
import datetime

canvas_token = "5590~PBI1RLqkpw2nf7ybBYAfyYHEKPPN1Q5QAGaORQK2xGOZTCQ96qmx2YR4MeNu5POJ"


def target(query):
    url = 'https://canvas.instructure.com/api/v1/' + query + '?access_token=' + canvas_token
    r = requests.get(url)
    return r


# get due date of current assignment and convert it to a datetime object.
def due_past(date_due):
    date = datetime.datetime.strptime(date_due, "%Y-%m-%dT%H:%M:%SZ")
    if date > datetime.datetime.now():
        return True


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

# break down each class list into assignments and get name, due date, class id,
# and possible link to assignment(might not work because canvas for CWRU has different url
current_assignments = []
for i in range(len(all_assignments)):
    for j in range(len(all_assignments[i])):
        if due_past(all_assignments[i][j]["due_at"]):
            current_assignments.append(all_assignments[i][j])

# adding course name to each assignment
# might need to shorten each course name
for i in range(len(current_assignments)):
    for j in range(len(course_list)):
        if current_assignments[i]["course_id"] == course_list[j]["id"]:
            current_assignments[i]["course_name"] = course_list[j]["name"]




