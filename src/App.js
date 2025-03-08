import dummy_image from "./assets/dummy_image.jpg";
import ImageViewerIncludingText from "./custom_components/image_viewer_including_text/ImageViewerIncludingText";
import "./App.css";
import { useEffect, useState } from "react";
import {
  get_generated_image,
  get_generated_story,
  get_generated_story_continuation,
} from "./api/story_apis/storyApis";
import CustomSpinnerComponent from "./custom_components/custom_spinner_component/CustomSpinnerComponent";
function App() {
  const [story, setStory] = useState({
    story_name: null,
    story_content: null,
    story_image: null,
  });
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStory();
  }, []);
  const fetchStory = async () => {
    try {
      setLoading(true);
      const story_response = await get_generated_story();
      const { story_name, story_line } = JSON.parse(story_response);
  
  
      if (story_line?.story_content) {
        const image_response = await get_generated_image(story_line?.story_image_prompt);
        console.log(image_response);
  
        setStory({
          story_name,
          story_content: story_line.story_content,
          story_image: image_response,
        });
      } else {
        fetchStory();
      }
    } catch (error) {
      console.error("Error fetching story:", error);
    } finally {
      setLoading(false);
    }
  };
  
  const fetchContiniousStory = async (user_input) => {
    try {
      setLoading(true);
      const story_response = await get_generated_story_continuation(user_input);
      const { story_name, story_line } = JSON.parse(story_response);
  
      console.log(story_line);
  
      if (story_line?.story_content) {
        const image_response = await get_generated_image(story_line?.story_image_prompt);
        console.log(image_response);
  
        setStory({
          story_name,
          story_content: story_line.story_content,
          story_image: image_response,
        });
  
        setUserInput("");
      }
    } catch (error) {
      console.error("Error fetching story:", error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="app_main_container">
      <div className="app_sub_container_v0">
        <div>
          <p className="app_story_title">{story.story_name}</p>
        </div>
        <div>
          <ImageViewerIncludingText
            image={story.story_image}
            text={story.story_content}
          />
        </div>
        <div className="app_input_container">
          <input
            className="app_input_field"
            placeholder="Type your next action"
            value={userInput}
            onChange={(e) => {
              setUserInput(e.target.value);
            }}
          />
          <button
            className="app_input_send_button"
            onClick={() => {
              fetchContiniousStory(userInput);
            }}
          >
            Send
          </button>
          <button className="app_input_reset_story_button" onClick={() => {
                fetchStory();
          }}>
            Reset Story
          </button>
        </div>
      </div>
      {loading && (
        <div className="app_sub_spinner_component">
          <CustomSpinnerComponent />
        </div>
      )}
    </div>
  );
}

export default App;
