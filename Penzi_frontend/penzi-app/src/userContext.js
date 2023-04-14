import { useContext,createContext,useState} from "react";

const userContext = createContext();
export const UserProvider=({children})=>{
    const [phoneNumber, setPhoneNumber] = useState('');
    return (
        <userContext.Provider value={{setPhoneNumber,phoneNumber}}>
            {children}
        </userContext.Provider>
    )
}
export const useUserContext=()=>{
    return useContext(userContext);
}
