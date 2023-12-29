using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;
using Microsoft.Extensions.Configuration;

#region Configs


var configs = new ConfigurationBuilder()
                .AddUserSecrets("pi azSpeech")
                .Build();



var speechConfig = SpeechTranslationConfig.FromSubscription(configs["key"],
                                                 configs["region"]);


speechConfig.SpeechRecognitionLanguage = "en-US";
speechConfig.AddTargetLanguage("hi-IN");

#endregion

using var audioConfig = AudioConfig.FromDefaultMicrophoneInput();
using var speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);


while (true)
{
    Console.WriteLine("\n\n\n\n\n\n\n\nSpeak now or forever hold your chickpeas");

    var result = await speechRecognizer.RecognizeOnceAsync();

    Console.WriteLine($"\n\n\nTime taken: {result.Duration.TotalSeconds}");
    Console.WriteLine($"Detected: {result.Text}");
    Console.WriteLine($"Reason: {result.Reason}");

}
