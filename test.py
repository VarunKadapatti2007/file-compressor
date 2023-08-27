from flask import Flask, render_template, request, send_file
import cloudconvert

app = Flask(__name__)

cloudconvert.configure(api_key='API_KEY_HERE', sandbox=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    job = cloudconvert.Job.create(payload={
        "tasks": {
            'upload-my-file': {
                'operation': 'import/upload'
            }
        }
    })

    if 'tasks' in job and isinstance(job['tasks'], dict):
        upload_task_id = list(job['tasks'].keys())[0]
        upload_task = cloudconvert.Task.find(id=upload_task_id)
        uploaded_file = request.files['file']

        temp_file_path = 'E:\\file_convert\\uploads\\' + uploaded_file.filename
        uploaded_file.save(temp_file_path)

        res = cloudconvert.Task.upload(file=temp_file_path, task=upload_task)

        exported_url_task_id = job['tasks'][upload_task_id]['output']['tasks'][0]['id']
        res = cloudconvert.Task.wait(id=exported_url_task_id)
        file = res.get("result").get("files")[0]
        res = cloudconvert.download(filename=file['filename'], url=file['url'])

        return send_file(
            res,
            as_attachment=True,
            download_name='compressed.pdf'
        )
    else:
        return "Error: Unable to retrieve task information from the CloudConvert API"

if __name__ == '__main__':
    app.run(debug=True)
