import React, { useEffect, useRef, useState } from 'react';
import { Device } from '@twilio/voice-sdk';

export default function TwilioCall() {
  const [device, setDevice] = useState(null);
  const [status, setStatus] = useState('loading');
  const connRef = useRef(null);
  const [identity, setIdentity] = useState('receiver');
  const [to, setTo] = useState('');

  useEffect(() => {
    async function init() {
      try {
        const res = await fetch(`/api/token/?identity=${encodeURIComponent(identity)}`);
        const data = await res.json();
        const twDevice = new Device(data.token);

        twDevice.on('registered', () => setStatus('ready'));
        twDevice.on('unregistered', () => setStatus('unregistered'));
        twDevice.on('error', (err) => {
          console.error('Twilio Device error', err);
          setStatus('error');
        });
        twDevice.on('incoming', (conn) => {
          if (window.confirm('Accept incoming call?')) {
            conn.accept();
            connRef.current = conn;
            setStatus('in-call');
            conn.on('disconnect', () => setStatus('ready'));
          } else {
            conn.reject();
          }
        });

        setDevice(twDevice);
      } catch (err) {
        console.error(err);
        setStatus('error-init');
      }
    }
    init();
  }, [identity]);

  const makeCall = () => {
    if (!device) return;
    setStatus('calling');
    const params = { To: to || 'receiver' };
    const conn = device.connect({ params });
    connRef.current = conn;
    conn.on('accept', () => setStatus('in-call'));
    conn.on('disconnect', () => setStatus('ready'));
  };

  const hangup = () => {
    if (connRef.current) {
      connRef.current.disconnect();
      connRef.current = null;
      setStatus('ready');
    }
  };

  return (
    <div>
      <div style={{ marginBottom: 12 }}>
        <label>
          Your identity:&nbsp;
          <input value={identity} onChange={(e) => setIdentity(e.target.value)} />
        </label>
      </div>
      <div style={{ marginBottom: 12 }}>
        <label>
          Call To (identity or +E.164 number):&nbsp;
          <input value={to} onChange={(e) => setTo(e.target.value)} placeholder="receiver or +12345566" />
        </label>
      </div>

      <div style={{ marginBottom: 12 }}>
        <button onClick={makeCall} disabled={!device || status==='calling' }>Call</button>
        <button onClick={hangup} style={{ marginLeft: 8 }}>Hangup</button>
      </div>

      <div>Status: <strong>{status}</strong></div>
    </div>
  );
}
