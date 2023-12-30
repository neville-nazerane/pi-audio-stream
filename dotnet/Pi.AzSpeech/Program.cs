﻿using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;
using Microsoft.Extensions.Configuration;

#region Configs


var configs = new ConfigurationBuilder()
                .AddUserSecrets("pi azSpeech")
                .Build();



var speechConfig = SpeechConfig.FromSubscription(configs["key"],
                                                 configs["region"]);


speechConfig.SpeechRecognitionLanguage = "en-US";

#endregion

using var keywordModel = KeywordRecognitionModel.FromFile("ML_Models");
using var audioConfig = AudioConfig.FromDefaultMicrophoneInput();

//using var keywordRecognizer = new KeywordRecognizer(audioConfig);


using var speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);

Console.WriteLine("SAY IT!");

//while (true)
//{
//    await keywordRecognizer.RecognizeOnceAsync(keywordModel);
//    Console.WriteLine("Oh hello there");
//}

while (true)
{
    Console.WriteLine("\n\n\n\n\n\n\n\nSpeak now or forever hold your chickpeas");

    var result = await speechRecognizer.RecognizeOnceAsync();

    Console.WriteLine($"\n\n\nTime taken: {result.Duration.TotalSeconds}");
    Console.WriteLine($"Detected: {result.Text}");
    Console.WriteLine($"Reason: {result.Reason}");

}
