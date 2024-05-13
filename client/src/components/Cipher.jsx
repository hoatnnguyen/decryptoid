import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Navbar from './Navbar'
import { useNavigate } from 'react-router-dom'

const Cipher = () => {
    // const accessToken = sessionStorage.getItem('accessToken');
    // console.log(accessToken)
    const navigate = useNavigate();

    const [inputText, setinputText] = useState('');
    const [cipherAlgorithm, setcipherAlgorithm] = useState(1);
    const [cipherMode, setCipherMode] = useState(1);
    const [key, setKey] = useState('');
    const [file, setFile] = useState(null);
    const [keyError, setKeyError] = useState('');
    const [submitError, setSubmitError] = useState('');
    const [outputText, setOutputText] = useState('');

    const [accessToken, setAccessToken] = useState('');

    // Effect to fetch accessToken from sessionStorage when component mounts
    useEffect(() => {
        const token = sessionStorage.getItem('accessToken');
        if (token) {
            setAccessToken(token);
        }
        else {
            navigate("/login");
        }
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!inputText.trim() && !file) {
            setSubmitError("Please enter text or select a file.");
            return;
        }

        if (inputText.trim() && file) {
            setSubmitError("Please only enter text or select a file, not both.");
            return;
        }

        if (!key.trim()) {
            setKeyError("Please enter a key.");
            return;
        }

        if (!inputText.trim() && file) {
            setSubmitError("");
            const formData = new FormData();
            formData.append(
                "file",
                file
            )
            formData.append(
                "cipherAlgo",
                cipherAlgorithm
            )
            formData.append(
                "key",
                key
            )
            formData.append(
                "cipherMode",
                cipherMode
            )
            formData.append(
                "accessToken",
                accessToken
            )

            console.log("FormData content:");
            for (const pair of formData.entries()) {
                console.log(pair[0] + ', ' + pair[1]);
            }

            try {
                // const response = await axios.post("http://127.0.0.1:8000/cipheractivity");
                const response = await axios.post("http://127.0.0.1:8000/cipheractivity/file", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                });
                console.log('Response from the backend:', response.data);
                setOutputText(response.data);
            } catch (error) {
                console.error('Error: ', error);
                setSubmitError(error.response.data.detail);
            }

        }
        if (inputText.trim() && !file) {
            setSubmitError("");
            const formData = new FormData();
            formData.append(
                "inputText",
                inputText
            )
            formData.append(
                "cipherAlgo",
                cipherAlgorithm
            )
            formData.append(
                "key",
                key
            )
            formData.append(
                "cipherMode",
                cipherMode
            )
            formData.append(
                "accessToken",
                accessToken
            )

            console.log("FormData content:");
            for (const pair of formData.entries()) {
                console.log(pair[0] + ', ' + pair[1]);
            }

            try {
                // const response = await axios.post("http://127.0.0.1:8000/cipheractivity");
                const response = await axios.post("http://127.0.0.1:8000/cipheractivity/inputText", formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                });
                console.log('Response from the backend:', response.data);
                setOutputText(response.data);
            } catch (error) {
                console.error('Error: ', error);
                setSubmitError(error.response.data.detail);
                setOutputText("");
            }
        }
    }

    // console.log(inputText);
    // console.log(file);
    console.log("cipher algorithm: ", cipherAlgorithm);
    console.log("key1: ", key);
    // console.log("cipher mode: ", cipherMode);
    // console.log("inputContent: ", inputContent)
    return (
        <div className="min-vh-100">
            <Navbar />
            <div className="d-flex justify-content-center align-items-center">
                <div className="container">
                    <div className="row">
                        <div className="col-sm-12 col-md-7 col-lg-8 mx-auto">
                            <div className="card border-0 shadow rounded-3 my-5">
                                <div className="card-body p-4 p-sm-5">
                                    <h1 className="card-title text-center mb-5">Cipher Tool</h1>
                                    {submitError && <div className="text-danger mb-2">{submitError}</div>}
                                    <form className="row g-3" onSubmit={handleSubmit}>
                                        <div className="form-floating mb-4">
                                            <textarea className="form-control" placeholder="Leave a comment here" id="floatingTextarea2" style={{ height: "200px" }}
                                                value={inputText}
                                                onChange={(e) => setinputText(e.target.value)}
                                            ></textarea>
                                            <label htmlFor="floatingTextarea2">Enter text here or select a .txt file to upload</label>
                                        </div>
                                        <div className="mb-3 col-md-5">
                                            <input type="file" className="form-control" id="file" accept=".txt"
                                                onChange={(e) => setFile(e.target.files[0])}
                                            />
                                        </div>
                                        <div className="mb-3 col-md-7">
                                            <select className="form-select mb-3" aria-label="Default select example"
                                                onChange={(e) => {
                                                    setcipherAlgorithm(e.target.value)
                                                }}
                                            >
                                                <option selected value="1">Simple Substitution</option>
                                                <option value="2">Double Transposition</option>
                                                <option value="3">RC4</option>
                                            </select>
                                        </div>
                                        <div className="form-floating mb-4">
                                            <input type="text" className={`form-control ${keyError && 'is-invalid'}`} id="key" placeholder="key"
                                                value={key}
                                                onChange={(e) => {
                                                    setKey(e.target.value);
                                                    setKeyError('');
                                                }}
                                            />
                                            <label htmlFor="key">Key</label>
                                            {keyError && <div className="invalid-feedback">{keyError}</div>}
                                        </div>
                                        <select className="form-select mb-3" aria-label="Default select example"
                                            onChange={(e) => {
                                                setCipherMode(e.target.value)
                                            }}
                                        >
                                            <option selected value="1">Encrypt</option>
                                            <option value="2">Decrypt</option>
                                        </select>
                                        <div className="d-grid">
                                            <button className="btn btn-primary btn-login text-uppercase fw-bold" type="submit">Submit</button>
                                        </div>
                                        {outputText && <div>{outputText}</div>}

                                        {/* <div className="mb-3 col-md-6 d-flex justify-content-center">
                                            <button className="btn btn-primary btn-login text-uppercase fw-bold" type="submit" onClick={handleSubmit}></button>
                                        </div>

                                        <div className="mb-3 col-md-6 d-flex justify-content-center">
                                            <button className="btn btn-primary btn-login text-uppercase fw-bold" type="submit">Decrypt</button>
                                        </div> */}
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Cipher
