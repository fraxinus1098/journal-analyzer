import { useState, FormEvent, ChangeEvent } from 'react';
import { uploadPDFs } from '@/lib/api';

export function UploadForm() {
    const [files, setFiles] = useState<File[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        
        try {
            await uploadPDFs(files);
            setFiles([]);
            alert('Upload successful!');
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Upload failed');
        } finally {
            setLoading(false);
        }
    };

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        const fileList = e.target.files;
        if (fileList) {
            setFiles(Array.from(fileList));
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <label 
                    htmlFor="file-upload" 
                    className="block text-sm font-medium text-gray-700"
                >
                    Upload Journal PDFs
                </label>
                <input
                    id="file-upload"
                    type="file"
                    multiple
                    accept=".pdf"
                    onChange={handleFileChange}
                    className="mt-1 block w-full"
                />
            </div>
            {error && (
                <div className="text-red-600 text-sm">{error}</div>
            )}
            <button
                type="submit"
                disabled={loading || files.length === 0}
                className={`
                    bg-blue-500 text-white px-4 py-2 rounded
                    disabled:opacity-50 hover:bg-blue-600
                    transition-colors duration-200
                `}
            >
                {loading ? 'Uploading...' : 'Upload'}
            </button>
        </form>
    );
} 