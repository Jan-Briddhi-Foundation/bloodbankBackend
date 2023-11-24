import { createSlice } from "@reduxjs/toolkit";


const initialState  = {
    entities : null,
    status:"idle"
}

const authReducer = createSlice({name:"auth", 
    initialState:initialState, reducers:{
        
        userLoaded(){}
    }
})