import { useState} from "react";
import BeatLoader from "react-spinners/BeatLoader";
import './customSpinnerComponentStyle.css'
function CustomSpinnerComponent() {
    const override= {
        display: "block",
        margin: "0 auto",
        borderColor: "red",
      };
      
  return (
    <div className="custom_spinner_main_container">
        <div>
        <BeatLoader
        color={"#2D99FF"}
        loading={true}
        cssOverride={override}
        size={25}
        aria-label="Loading Spinner"
        data-testid="loader"
        />
        </div>
    </div>
  )
}

export default CustomSpinnerComponent