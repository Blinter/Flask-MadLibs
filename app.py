from flask import Flask, request, render_template
# from flask_debugtoolbar import DebugToolbarExtension
from stories import Story
from generatedstories import GeneratedStories

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

# debug = DebugToolbarExtension(app)

global stories_init_class, stories_qs, stories_choices


def seed_stories():
    """Initialize Stories and seed quick select + choices"""
    global stories_init_class, stories_qs, stories_choices
    stories_init_class = GeneratedStories()
    stories_qs = stories_init_class.quick_select_stories
    stories_choices = stories_init_class.quick_select_required_items


seed_stories()


@app.route('/', methods=['GET'])
def story_home():
    """Returns Story Prompt"""
    story_selected = request.args.get("id_select", False)
    stories_results = [request.args.get("i" + str(i), False) for i in
                       range(0, len(stories_choices[int(story_selected)]))]
    found_story = any(stories_results) if story_selected else False
    if not story_selected and not found_story:
        if request.args.get("seed_new", False):
            seed_stories()
        return render_template("story.html", choices=stories_init_class.sampled_amount)
    elif (story_selected and not found_story and
          len(stories_choices) - 1 >= int(story_selected) >= 0):
        if request.args.get("seed_new", False):
            seed_stories()
        return render_template("story.html",
                               idx=story_selected,
                               ask=stories_choices[int(story_selected)])
    else:
        return render_template(
            "story.html",
            results=Story(stories_choices[int(story_selected)], stories_qs[int(story_selected)]).generate({
                stories_choices[int(story_selected)][int(i)]:
                stories_results[i]
                for i in range(0, len(stories_choices[int(story_selected)]))}))


"""
Snippet for adding story (editing)
results=Story(stories_choices[int(story_selected)],
stories_qs[int(story_selected)]).generate({
stories_choices[int(story_selected)][int(i)]:
"[[[" + stories_choices[int(story_selected)][int(i)] + "]]]"
for i in range(0, len(stories_choices[int(story_selected)]))})                               
"""