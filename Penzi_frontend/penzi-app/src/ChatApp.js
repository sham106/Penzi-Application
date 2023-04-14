import './App.css';
import {Button, Card, Col, Container, Form, Row} from "react-bootstrap";
import PenziIcon from './PenziIcon.jpg';
import CardHeader from 'react-bootstrap/esm/CardHeader';
import {MdOutlineSendToMobile} from "react-icons/md";
import axios from 'axios'
import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
// import { useUserContext } from './userContext';

function ChatApp({phoneNumber}) {

  // sendMessage
  // 1. Validation
  //   - Add to messages
  // 2. Post to backend
  //    - calling postData
  // 3. Check if error happened
  //    - Show alert if it happened, 
  // 4. Add entry to messages

  // Scrolling
  const [userMessage, setUserMessage] = useState('');
  const [messages, setMessages] = useState([{text:'WELCOME AT PENZI, to get started send the word PENZI', timestamp: new Date(), isServerRespose:true}])
  const [timestamp, setTimestamp] = useState(new Date(Date.now()));
  const navigate = useNavigate
  // const {phoneNumber}=useUserContext();

  const chatContainerRef = useRef(null)
  // console.log(phoneNumber)

  useEffect(() => {
    chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
  },[messages]);

  // if(!phoneNumber){
  //   navigate('/');
  //   return null;
  // }
 
  const SendMessage = (event) => {
    event.preventDefault();

    axios.post(`${process.env.REACT_APP_BACKEND_URL}/penzi`,{
      'phone_number':phoneNumber,
      'message':userMessage,
    })
      .then(response => {
        console.log('response received', response.data);
        console.log('Date is : ', response.data.timestamp);

        const serverMessage = {
          text: response.data.reply,
          timestamp: timestamp,
          isServerRespose: true
        }

        setMessages([...messages,{text: userMessage, timestamp},serverMessage]);
        setUserMessage('');

      })
      .catch(error => {
        console.error(error);
        return ({isServerRespose:true,hasError:true,msg:'Error happened'})
      });
      
    
      const formatedtimestamp = timestamp.toLocaleString("en-US",{
        day: "2-digit",
        month: "short",
        hour: "numeric",
        minute: "numeric",
        hour12: true,
      })
      
  }

  return (
    <>
    <Container style={{backgroundColor: 'white'}}>
      <Row className='d-flex justify-content-center' >
        <Col md="8" lg="6" xl="4" >
          <Card className='shadow' style = {{  top:'2rem'}}  >
            <CardHeader className='d-flex justify-content-center p-3 align-items-center'  >
              <img src={PenziIcon} className='rounded-circle ' width={40} alt='penzi icon'></img>
              <div style={{display: 'block'}}>
              <h6 className='px-4 ' style={{color:'#0A1E80'}}>Meet the person of your dream</h6>
              </div>
            </CardHeader>
            <Card.Body ref={chatContainerRef} style={{height:'400px',  overflowY:'auto', }}>
              {/* // Information on how to start

              // Loop over the messages
              // Update the message fields
              // isRemote help to style  */}
              {messages.map((msg, index) => (
                <div key={index} className={`d-flex py-1 ${msg.isServerRespose ? 'justify-content-start' :  'justify-content-end'} `} >
                <div  className="small p-2 ms-3  rounded-3 justify-content-end "
                style={{maxWidth:'90%', background: msg.isServerRespose ? '#00C851': '#ede7f6', color: msg.isServerRespose ? 'white' : 'black', display:'inline-block'}}>
                  {msg.text}
                  <span className='d-flex justify-content-end pt-0.5'>
                    <p className="small mb-1 text-muted">{new Date(msg.timestamp).toLocaleString()}</p>
                  </span>
                </div>
                </div>
                
              ))}
              
            </Card.Body>
            <Card.Footer  >
               {/* // Update data on input */}
              <Form className='d-flex align-items-center' onSubmit={SendMessage}>
                <Form.Group className='flex-grow-1 '>
                  <Form.Control type= 'text' placeholder='Type your message' 
                  value={userMessage} onChange = {event => setUserMessage(event.target.value)}>
                  </Form.Control>
                </Form.Group>
                
                <Button  type='submit'  className='rounded-5 d-flex justify-content-center hover-overlay'
                 style={{ background:'#1B5E20', border:'none', 
                  marginLeft:'0.5rem', justifyContent:'center'}} 
                  disabled={!userMessage}  >
                  <MdOutlineSendToMobile color='white' size={20} />
                </Button> 
              </Form>
            </Card.Footer>
          </Card>
        </Col>      
      </Row>
    </Container>
    </>
  );
}

export default ChatApp;
