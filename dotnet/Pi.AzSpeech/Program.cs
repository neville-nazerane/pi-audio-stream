﻿using Microsoft.CognitiveServices.Speech;
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

while (true) await WaitForKeywordAsync();

//while (true)
//{
//    await keywordRecognizer.RecognizeOnceAsync(keywordModel);
//    Console.WriteLine("Oh hello there");
//}


//while (true)
//{

//    await WaitForKeywordAsync();


//    using var audioConfig2 = AudioConfig.FromDefaultMicrophoneInput();
//    using var speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig2);
//    var result = await speechRecognizer.RecognizeOnceAsync();

//    Console.WriteLine($"\n\n\nTime taken: {result.Duration.TotalSeconds}");
//    Console.WriteLine($"Detected: {result.Text}");
//    Console.WriteLine($"Reason: {result.Reason}");

//}


Task WaitForKeywordAsync()
{
    using var audioConfig = AudioConfig.FromDefaultMicrophoneInput();
    using var keywordRecognizer = new KeywordRecognizer(audioConfig);
    return keywordRecognizer.RecognizeOnceAsync(keywordModel);
    Console.WriteLine("now listening...");

}



static string GetCurrentFolder() 
    => Directory.GetCurrentDirectory()
                       .Split(["/bin/", "/bin/"], StringSplitOptions.None)
                       .First();