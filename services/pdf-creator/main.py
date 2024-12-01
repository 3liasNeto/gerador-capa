from flask import Flask, render_template, request, Response
from generate_pdf import GeneratePDF
import io
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/generate": {"origins": "http://localhost:5173", "allow_headers": ["Content-Type"]}})

@app.route("/generate", methods=['POST'])
def generatePDF():
    data = request.get_json()
    field_dict ={
            "course": data['course'],
            "matter": data['matter'],
            "name": data['name'],
            "id": data['id'],
            "city": data['city'],
        }
    pdf = GeneratePDF("sample.pdf")
    
    pdf.open_page(
        field_dict['course'], 
        field_dict['matter'], 
        field_dict['name'], 
        field_dict['id'], 
        field_dict['city']
    )
    
    modified_pdf_stream = io.BytesIO()
    pdf.doc.save(modified_pdf_stream)
    modified_pdf_stream.seek(0)

    return Response(
        modified_pdf_stream,
        mimetype='application/pdf',
        headers={'Content-Disposition': 'attachment; filename="modified_cover.pdf"'}
    )

if __name__ == "__main__":
    app.run(debug=True)