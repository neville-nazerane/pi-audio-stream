using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;
using Microsoft.Extensions.Configuration;
using System.Reflection;

#region Configs


var configs = new ConfigurationBuilder()
                .AddUserSecrets("pi azSpeech")
                .Build();



var speechConfig = SpeechConfig.FromSubscription(configs["key"],
                                                 configs["region"]);


speechConfig.SpeechRecognitionLanguage = "en-US";

#endregion

var modelPath = Path.Combine(GetCurrentFolder(),
                             "ML_Models",
                             "keyword.table");

Console.WriteLine(File.Exists(modelPath) ? "Found the file" : "FILE NOT FOUND!!!");

using var keywordModel = KeywordRecognitionModel.FromFile(modelPath);




Console.WriteLine("SAY IT!");

using var audioConfig = AudioConfig.FromDefaultMicrophoneInput();
using var speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);
speechRecognizer.Recognized += SpeechRecognizer_Recognized;
await speechRecognizer.StartKeywordRecognitionAsync(keywordModel);

Console.WriteLine("Alright.... listening now...");

await Task.Delay(Timeout.Infinite);

//await speechRecognizer.StartContinuousRecognitionAsync();


void SpeechRecognizer_Recognized(object? sender, SpeechRecognitionEventArgs e)
{
    var result = e.Result;
    Console.WriteLine($"\n\n\nTime taken: {result.Duration.TotalSeconds}");
    Console.WriteLine($"Detected: {result.Text}");
    Console.WriteLine($"Reason: {result.Reason}");
}


//while (true) await WaitForKeywordAsync();

//while (true)
//{
//    await keywordRecognizer.RecognizeOnceAsync(keywordModel);
//    Console.WriteLine("Oh hello there");
//}


//using var audioConfig = AudioConfig.FromDefaultMicrophoneInput();
//using var speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);
//while (true)
//{

//    //await WaitForKeywordAsync();


//    //using var audioConfig2 = AudioConfig.FromDefaultMicrophoneInput();
//    speechRecognizer.Recognized += SpeechRecognizer_Recognized;
//    await speechRecognizer.StartKeywordRecognitionAsync(keywordModel);


//    //Console.WriteLine($"\n\n\nTime taken: {result.Duration.TotalSeconds}");
//    //Console.WriteLine($"Detected: {result.Text}");
//    //Console.WriteLine($"Reason: {result.Reason}");

//}




//async Task WaitForKeywordAsync()
//{
//    using var keywordRecognizer = new KeywordRecognizer(audioConfig);
//    await keywordRecognizer.RecognizeOnceAsync(keywordModel);

//    Console.WriteLine("now listening...");

//}



static string GetCurrentFolder() 
    => Directory.GetCurrentDirectory()
                       .Split(["/bin/", "/bin/"], StringSplitOptions.None)
                       .First();