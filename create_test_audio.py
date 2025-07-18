from gtts import gTTS
import os

def create_test_audio():
    """
    Create a test sales call audio file using text-to-speech.
    """
    # Sample sales conversation
    text = """
    Hi, good afternoon. This is Sindhuja from CloudWorks.

Yeah, I just got off a call with the CTO of FinNext last week — um, I think his name was Rajiv — and he seemed really interested in moving to a hybrid cloud model. 

He specifically asked about AWS Outposts versus Azure Arc. So, I told him we’d get back with a detailed comparison soon. Can you pull up the key differences between those two platforms?

Also, I need to set up a follow-up meeting with him. Let’s go ahead and schedule that for Friday, 2:30 PM. Title it ‘FinNext Cloud Proposal Follow-up’.

Oh, and before I forget — I’m also speaking at the Tech Innovations Summit next Monday. Can you check the latest enterprise cloud adoption stats for 2025? I wanna include that in my presentation.

Mmm, yeah — also set a reminder for me tomorrow at 7 PM to send the draft deck to the team, okay?

One more thing — check if any of our competitors have announced new cloud partnerships recently. Anything with AWS or Microsoft?

And finally, ask Gemini to generate a few bullet points I could include in the FinNext proposal — focus mainly on security, scalability, and maybe ease of migration.

Okay, that’s all for now — thanks!

    """
    
    # Create samples directory if it doesn't exist
    if not os.path.exists("samples"):
        os.makedirs("samples")
    
    # Generate speech
    tts = gTTS(text=text, lang='en', slow=False)
    
    # Save the file
    file_path = os.path.join("samples", "test_sales_call_2.mp3")
    tts.save(file_path)
    print(f"Test audio file created at: {file_path}")
    return file_path

if __name__ == "__main__":
    create_test_audio() 