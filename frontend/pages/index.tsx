import { useEffect, useState } from "react";

const API = "/api";

interface UploadedFile {
  name: string;
  size_kb: number;
}

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [status, setStatus] = useState("");
  const [previewContent, setPreviewContent] = useState("");
  const [gptResponse, setGptResponse] = useState("");

  const fetchFiles = async () => {
    try {
      const res = await fetch(`${API}/files`);
      const data = await res.json();
      setUploadedFiles(data.files || []);
    } catch (err) {
      setStatus("❌ Failed to fetch files");
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleUpload = async () => {
    setStatus("📤 Uploading...");
    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    const res = await fetch(`${API}/upload`, {
      method: "POST",
      body: formData,
    });

    if (res.ok) {
      setStatus("✅ Upload successful!");
      fetchFiles();
    } else {
      setStatus("❌ Upload failed.");
    }
  };

  const handlePreview = async (filename: string) => {
    const res = await fetch(`${API}/files/${filename}/preview`);
    const data = await res.json();
    setPreviewContent(data.content || "Could not load preview.");
  };

  const handleSendToGpt = async (filename: string) => {
    setStatus("🤖 Talking to GPT...");
    const res = await fetch(`${API}/files/${filename}/gpt`, {
      method: "POST",
    });
    const data = await res.json();
    setGptResponse(data.gpt_response || "No response from GPT.");
    setStatus("✅ GPT response received!");
  };

  const handleDelete = async (filename: string) => {
    const res = await fetch(`${API}/files/${filename}`, {
      method: "DELETE",
    });

    if (res.ok) {
      setStatus(`🗑️ Deleted ${filename}`);
      fetchFiles();
    } else {
      setStatus("❌ Failed to delete.");
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  return (
    <main style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>📚 One-Click Book Generator</h1>

      <p>Upload Lore, Overview, Chapters, or Plot files:</p>
      <input type="file" multiple onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ marginLeft: "1rem" }}>
        Upload
      </button>
      <p>{status}</p>

      <hr />

      <h2>📂 Uploaded Files</h2>
      <ul>
        {uploadedFiles.map((file) => (
          <li key={file.name}>
            <strong>{file.name}</strong> ({file.size_kb} KB)
            <button onClick={() => handlePreview(file.name)} style={{ marginLeft: "1rem" }}>
              📃 Preview
            </button>
            <button onClick={() => handleSendToGpt(file.name)} style={{ marginLeft: "0.5rem" }}>
              🤖 Send to GPT
            </button>
            <button onClick={() => handleDelete(file.name)} style={{ marginLeft: "0.5rem" }}>
              🗑️ Delete
            </button>
          </li>
        ))}
      </ul>

      {previewContent && (
        <>
          <h3>📄 Preview</h3>
          <textarea
            value={previewContent}
            readOnly
            style={{ width: "100%", height: "200px", marginBottom: "1rem" }}
          />
        </>
      )}

      {gptResponse && (
        <>
          <h3>🤖 GPT Response</h3>
          <textarea
            value={gptResponse}
            readOnly
            style={{ width: "100%", height: "200px" }}
          />
        </>
      )}
    </main>
  );
}
