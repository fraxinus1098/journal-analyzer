// Add type definitions
interface UploadResponse {
    success: boolean;
    message: string;
}

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

export async function uploadPDFs(files: File[]): Promise<UploadResponse> {
    if (!files.length) {
        throw new Error('No files selected');
    }

    const formData = new FormData();
    files.forEach(file => {
        // Validate file type
        if (!file.type.includes('pdf')) {
            throw new Error('Only PDF files are allowed');
        }
        formData.append('files', file);
    });

    try {
        const response = await fetch(`${API_BASE_URL}/api/upload`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || 'Upload failed');
        }

        return response.json();
    } catch (error) {
        console.error('Upload error:', error);
        throw error;
    }
} 