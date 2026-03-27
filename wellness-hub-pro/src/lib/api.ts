const BASE_URL = "http://localhost:8000";
const PATIENT_ID = "P001";

const headers = {
  "Content-Type": "application/json",
  "X-Patient-ID": PATIENT_ID,
};

export const api = {
  chat: async (message: string, onChunk: (text: string) => void) => {
    const res = await fetch(`${BASE_URL}/api/v1/chat`, {
      method: "POST",
      headers,
      body: JSON.stringify({ message }),
    });
    if (!res.ok) throw new Error("Chat request failed");
    const reader = res.body?.getReader();
    if (!reader) return;
    const decoder = new TextDecoder();
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      onChunk(decoder.decode(value));
    }
  },

  getProfile: async () => {
    const res = await fetch(`${BASE_URL}/api/v1/patient/${PATIENT_ID}/profile`, { headers });
    if (!res.ok) throw new Error("Failed to fetch profile");
    return res.json();
  },

  logSymptoms: async (data: Record<string, unknown>) => {
    const res = await fetch(`${BASE_URL}/api/v1/patient/${PATIENT_ID}/symptoms`, {
      method: "POST", headers, body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to log symptoms");
    return res.json();
  },

  logNutrition: async (data: Record<string, unknown>) => {
    const res = await fetch(`${BASE_URL}/api/v1/patient/${PATIENT_ID}/nutrition`, {
      method: "POST", headers, body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to log nutrition");
    return res.json();
  },

  logFitness: async (data: Record<string, unknown>) => {
    const res = await fetch(`${BASE_URL}/api/v1/patient/${PATIENT_ID}/fitness`, {
      method: "POST", headers, body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to log fitness");
    return res.json();
  },

  submitMentalHealth: async (data: Record<string, unknown>) => {
    const res = await fetch(`${BASE_URL}/api/v1/patient/${PATIENT_ID}/mental-health`, {
      method: "POST", headers, body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to submit screening");
    return res.json();
  },

  uploadDocument: async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch(`${BASE_URL}/api/v1/patient/${PATIENT_ID}/upload`, {
      method: "POST",
      headers: { "X-Patient-ID": PATIENT_ID },
      body: formData,
    });
    if (!res.ok) throw new Error("Upload failed");
    return res.json();
  },

  fetchHealthRecords: async () => {
    const res = await fetch(`${BASE_URL}/api/v1/health-records/fetch`, { headers });
    if (!res.ok) throw new Error("Failed to fetch health records");
    return res.json();
  },

  getHospitalStatus: async () => {
    const res = await fetch(`${BASE_URL}/api/v1/hospital/status`, { headers });
    if (!res.ok) throw new Error("Failed to fetch hospital status");
    return res.json();
  },
};
