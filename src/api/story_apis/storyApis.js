import { axiosClient } from "../apiconfig"

export const get_generated_story=async ()=>{
    try {
        let response=await axiosClient.get('generate_story')
        return response?.data?.story?.content
    } catch (error) {
        throw error
    }
}


export const get_generated_image=async (prompt)=>{
    try {
        let response=await axiosClient.post('generate_story_image',{ prompt })
        let image=response?.data?.image_url
        return process.env.REACT_APP_API_BASE_URL+image
    } catch (error) {
        throw error
    }
}

export const get_generated_story_continuation=async (prompt)=>{
    try {
        let response=await axiosClient.post('generate_story_continuation',{prompt})
        return response?.data?.story?.content
    } catch (error) {
        throw error
    }
}