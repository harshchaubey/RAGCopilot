import { useState, useEffect } from "react";
import { documentsApi } from "../services/api";

function AccessBadge({ level }) {
  const cls = { admin: "badge-admin", employee: "badge-employee", all: "badge-all" };
  return <span className={`badge ${cls[level] || ""}`}>{level}</span>;
}

export default function DocumentsPage() {
  const [docs, setDocs] = useState([]);
  const [form, setForm] = useState({ title: "", access_level: "all", file: null });
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const load = () => documentsApi.list().then((r) => setDocs(r.data)).catch(() => {});

  useEffect(() => { load(); }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!form.file || !form.title) return;
    setError("");
    setUploading(true);
    try {
      const fd = new FormData();
      fd.append("file", form.file);
      fd.append("title", form.title);
      fd.append("access_level", form.access_level);
      await documentsApi.upload(fd);
      setForm({ title: "", access_level: "all", file: null });
      e.target.reset();
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (docId) => {
    if (!confirm("Delete this document and all its indexed chunks?")) return;
    await documentsApi.delete(docId);
    await load();
  };

  return (
    <div className="page">
      <div className="page-header">
        <h1>Documents</h1>
      </div>

      <div className="upload-form">
        <h3>Upload Document</h3>
        {error && <div className="error-msg">{error}</div>}
        <form onSubmit={handleUpload}>
          <div className="upload-form-row">
            <div className="form-group">
              <label>Title</label>
              <input
                value={form.title}
                onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
                placeholder="Document title"
                required
              />
            </div>
            <div className="form-group">
              <label>Access Level</label>
              <select
                value={form.access_level}
                onChange={(e) => setForm((f) => ({ ...f, access_level: e.target.value }))}
              >
                <option value="admin">Admin only</option>
                <option value="employee">Admin + Employees</option>
                <option value="all">Everyone</option>
              </select>
            </div>
            <div className="form-group">
              <label>File (PDF, DOCX, TXT)</label>
              <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={(e) => setForm((f) => ({ ...f, file: e.target.files[0] }))}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary" style={{ width: "auto" }} disabled={uploading}>
              {uploading ? "Uploading..." : "Upload"}
            </button>
          </div>
        </form>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>File</th>
              <th>Access</th>
              <th>Chunks</th>
              <th>Uploaded By</th>
              <th>Date</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {docs.length === 0 && (
              <tr><td colSpan={7} style={{ textAlign: "center", color: "#888", padding: "24px" }}>No documents uploaded yet</td></tr>
            )}
            {docs.map((doc) => (
              <tr key={doc.document_id}>
                <td><strong>{doc.title}</strong></td>
                <td style={{ color: "#888" }}>{doc.filename}</td>
                <td><AccessBadge level={doc.access_level} /></td>
                <td>{doc.chunk_count}</td>
                <td>{doc.uploaded_by_email}</td>
                <td>{new Date(doc.uploaded_at).toLocaleDateString()}</td>
                <td>
                  <button className="btn btn-danger btn-sm" onClick={() => handleDelete(doc.document_id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
