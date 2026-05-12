import { useState, useEffect } from 'react';
import axios from 'axios';

const AudioUploader = () => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [loadingMessage, setLoadingMessage] = useState("");
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);
    
    // Correction state
    const [editedData, setEditedData] = useState({
        diagnosis: '',
        symptoms: '',
        medications: '',
        notes: ''
    });
    const [recordId, setRecordId] = useState(null);
    const [saving, setSaving] = useState(false);
    const [saveSuccess, setSaveSuccess] = useState(false);

    const loadingMessages = [
        " Transcribing audio...",
        " Analyzing medical data...",
        " Extracting entities..."
    ];

    useEffect(() => {
        let interval;
        if (loading) {
            let index = 0;
            setLoadingMessage(loadingMessages[0]);
            interval = setInterval(() => {
                index = (index + 1) % loadingMessages.length;
                setLoadingMessage(loadingMessages[index]);
            }, 2500);
        }
        return () => clearInterval(interval);
    }, [loading]);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setResponse(null);
        setError(null);
        setSaveSuccess(false);
    };

    const handleUpload = async () => {
        if (!file) {
            setError('Please select an audio file first.');
            return;
        }

        setLoading(true);
        setError(null);
        setResponse(null);
        setSaveSuccess(false);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await axios.post('http://127.0.0.1:8000/process-audio', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            if (res.data.status === 'no_speech_detected') {
                setError('No speech detected in the audio file.');
            } else {
                setResponse(res.data);
                setRecordId(res.data.record_id);
                
                // Initialize editable data
                const sd = res.data.structured_data;
                setEditedData({
                    diagnosis: sd?.diagnosis || '',
                    symptoms: sd?.symptoms?.join(', ') || '',
                    medications: sd?.medications?.join(', ') || '',
                    notes: sd?.notes || ''
                });
            }
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || 'An error occurred during processing.');
        } finally {
            setLoading(false);
        }
    };

    const handleSaveCorrection = async () => {
        if (!recordId) return;

        setSaving(true);
        setError(null);
        setSaveSuccess(false);

        const payload = {
            diagnosis: editedData.diagnosis,
            symptoms: editedData.symptoms.split(',').map(s => s.trim()).filter(s => s !== ""),
            medications: editedData.medications.split(',').map(s => s.trim()).filter(s => s !== ""),
            notes: editedData.notes
        };

        try {
            await axios.put(`http://127.0.0.1:8000/record/${recordId}/correct`, payload);
            setSaveSuccess(true);
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.detail || 'Failed to save correction.');
        } finally {
            setSaving(false);
        }
    };

    const structuredData = response?.structured_data;

    const styles = {
        container: {
            padding: '40px 20px',
            maxWidth: '750px',
            margin: '0 auto',
            fontFamily: 'system-ui, -apple-system, sans-serif',
            color: '#333',
            lineHeight: '1.6'
        },
        card: {
            backgroundColor: '#fafafa',
            borderRadius: '12px',
            padding: '25px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
            border: '1px solid #eee',
            textAlign: 'left',
            marginTop: '20px'
        },
        sectionTitle: {
            fontSize: '20px',
            fontWeight: 'bold',
            borderBottom: '2px solid #e0e0e0',
            paddingBottom: '8px',
            marginBottom: '15px',
            marginTop: '25px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
        },
        diagnosis: {
            fontSize: '22px',
            fontWeight: '800',
            color: '#2e7d32',
            margin: '5px 0'
        },
        icdCode: {
            fontSize: '16px',
            color: '#555',
            backgroundColor: '#e8f5e9',
            padding: '4px 10px',
            borderRadius: '6px',
            display: 'inline-block',
            marginBottom: '15px'
        },
        label: {
            fontWeight: 'bold',
            color: '#666',
            fontSize: '14px',
            textTransform: 'uppercase',
            letterSpacing: '0.5px',
            display: 'block',
            marginBottom: '4px'
        },
        transcriptBox: {
            backgroundColor: '#fff',
            padding: '15px',
            borderRadius: '8px',
            border: '1px solid #ddd',
            fontSize: '15px',
            fontStyle: 'italic',
            marginBottom: '20px'
        },
        list: {
            paddingLeft: '20px',
            margin: '0'
        },
        listItem: {
            marginBottom: '8px'
        },
        errorBox: {
            color: '#d32f2f',
            backgroundColor: '#ffebee',
            padding: '15px',
            borderRadius: '8px',
            border: '1px solid #ffcdd2',
            marginBottom: '20px',
            fontWeight: '500'
        },
        successBox: {
            color: '#2e7d32',
            backgroundColor: '#e8f5e9',
            padding: '15px',
            borderRadius: '8px',
            border: '1px solid #c8e6c9',
            marginBottom: '20px',
            fontWeight: '500'
        },
        loadingText: {
            fontSize: '18px',
            color: '#1976d2',
            fontWeight: '500',
            marginTop: '20px'
        },
        input: {
            width: '100%',
            padding: '10px',
            borderRadius: '6px',
            border: '1px solid #ccc',
            fontSize: '16px',
            marginBottom: '15px',
            boxSizing: 'border-box'
        },
        textarea: {
            width: '100%',
            padding: '10px',
            borderRadius: '6px',
            border: '1px solid #ccc',
            fontSize: '15px',
            minHeight: '80px',
            marginBottom: '15px',
            fontFamily: 'inherit',
            boxSizing: 'border-box'
        },
        saveButton: {
            padding: '12px 24px',
            fontSize: '16px',
            fontWeight: '600',
            backgroundColor: saving ? '#ccc' : '#1b5e20',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: saving ? 'not-allowed' : 'pointer',
            marginTop: '10px'
        }
    };

    const renderList = (items) => {
        if (!items || items.length === 0) {
            return <p style={{ color: '#888', fontStyle: 'italic' }}>None identified</p>;
        }
        return (
            <ul style={styles.list}>
                {items.map((item, index) => (
                    <li key={index} style={styles.listItem}>{item}</li>
                ))}
            </ul>
        );
    };

    return (
        <div style={styles.container}>
            <h1 style={{ textAlign: 'center', marginBottom: '30px' }}>⚕️ Medical AI Scribe</h1>
            
            <div style={{ 
                backgroundColor: '#fff', 
                padding: '20px', 
                borderRadius: '10px', 
                border: '1px solid #ddd',
                display: 'flex',
                flexDirection: 'row',
                alignItems: 'center',
                gap: '10px'
            }}>
                <input 
                    type="file" 
                    accept="audio/*" 
                    onChange={handleFileChange} 
                    style={{ fontSize: '16px' }}
                />
                <button 
                    onClick={handleUpload} 
                    disabled={loading || !file}
                    style={{ 
                        padding: '10px 24px',
                        fontSize: '16px',
                        fontWeight: '600',
                        backgroundColor: loading ? '#ccc' : '#2c3e50',
                        color: 'white',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: loading ? 'not-allowed' : 'pointer',
                        transition: 'background-color 0.2s'
                    }}
                >
                    {loading ? 'Processing...' : 'Start Analysis'}
                </button>
            </div>

            {loading && <div style={styles.loadingText}>{loadingMessage}</div>}

            {error && (
                <div style={styles.errorBox}>
                    ⚠️ {error}
                </div>
            )}

            {saveSuccess && (
                <div style={styles.successBox}>
                    ✅ Correction saved successfully
                </div>
            )}

            {response && (
                <div style={styles.card}>
                    <div style={styles.sectionTitle}>🧾 Clinical Summary</div>
                    
                    <div style={{ marginBottom: '20px' }}>
                        <span style={styles.label}>Transcript</span>
                        <div style={styles.transcriptBox}>"{response.transcript}"</div>
                    </div>

                    <div style={styles.sectionTitle}>AI Analysis</div>

                    <div style={{ marginBottom: '20px' }}>
                        <span style={styles.label}>Diagnosis</span>
                        <div style={styles.diagnosis}>{structuredData?.diagnosis || 'N/A'}</div>
                        
                        <span style={styles.label}>ICD-10 Code</span>
                        <div style={styles.icdCode}>{response.icd_code || 'N/A'}</div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
                        <div>
                            <span style={styles.label}>Symptoms</span>
                            {renderList(structuredData?.symptoms)}
                        </div>
                        <div>
                            <span style={styles.label}>Medications</span>
                            {renderList(structuredData?.medications)}
                        </div>
                    </div>

                    {structuredData?.notes && (
                        <div>
                            <span style={styles.label}>Clinical Notes</span>
                            <p style={{ backgroundColor: '#fff', padding: '12px', borderRadius: '8px', border: '1px solid #eee' }}>
                                {structuredData.notes}
                            </p>
                        </div>
                    )}

                    <div style={styles.sectionTitle}>✏️ Doctor Correction</div>
                    
                    <div>
                        <label style={styles.label}>Diagnosis</label>
                        <input 
                            style={styles.input} 
                            value={editedData.diagnosis}
                            onChange={(e) => setEditedData({...editedData, diagnosis: e.target.value})}
                        />

                        <label style={styles.label}>Symptoms (comma separated)</label>
                        <textarea 
                            style={styles.textarea} 
                            value={editedData.symptoms}
                            onChange={(e) => setEditedData({...editedData, symptoms: e.target.value})}
                        />

                        <label style={styles.label}>Medications (comma separated)</label>
                        <textarea 
                            style={styles.textarea} 
                            value={editedData.medications}
                            onChange={(e) => setEditedData({...editedData, medications: e.target.value})}
                        />

                        <label style={styles.label}>Clinical Notes</label>
                        <textarea 
                            style={styles.textarea} 
                            value={editedData.notes}
                            onChange={(e) => setEditedData({...editedData, notes: e.target.value})}
                        />

                        <button 
                            style={styles.saveButton}
                            onClick={handleSaveCorrection}
                            disabled={saving}
                        >
                            {saving ? 'Saving...' : 'Save Correction'}
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AudioUploader;
