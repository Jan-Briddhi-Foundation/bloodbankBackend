import { configureStore } from "@reduxjs/toolkit";
import 
const store = configureStore({reducer:{
    auth : authReducer
}})