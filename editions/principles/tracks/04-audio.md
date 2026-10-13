# Audio

The text is correct for a recording, but its exported clip cuts off the first word. The label is now wrong for the actual input. Sound data need source time and sample meaning, not only a transcript column.

## Work an authored waveform interval

Use this eight-sample, single-channel illustrative waveform at 8 samples per second: [0,0,1,-1,1,-1,0,0]. Amplitudes are dimensionless normalized sample values. It represents a toy pulse, not speech or a measured recording. Sample indices are 0–7; the recording spans [0,1) seconds. The half-open source-frame interval [2,6) contains four samples [1,-1,1,-1], starts at 0.25 seconds, ends at 0.75 seconds and lasts 0.5 seconds. Its target is the class “pulse”.

A manifest that stores end frame 6 inclusively yields five samples and 0.625 seconds. Both interpretations can load, so the interval convention must be explicit. A producer that relabels the same eight samples as 16 samples/s halves duration and changes their physical time spacing; that is not resampling. Proper resampling derives a different waveform under a specified reconstruction/filtering method. Do not silently apply amplitude normalization if loudness is part of the target.

This interval exercise establishes indexing and duration only. It does not establish speech alignment, acoustic realism or recognition quality. A later listening check must inspect the emitted waveform after every transformation.

## Carry this project through core 9–15

- Core 9: collect meaningful independent sessions/speakers or authored signal families; count unique recording time separately from multiple task views.
- Core 10: time shifts require corresponding target timestamps; noise augmentation needs a task-specific validity check.
- Core 11: ASR proposes words; a resolved transcript of the exact interval is the reference, not the model confidence.
- Core 12: verify generated content and allowed voice use; waveform validity alone cannot verify spoken words.
- Core 13: analyze boundary, silence/hallucination, speaker and language failures separately; protect the appropriate recording/session/script families.
- Core 14: freeze source and canonical hashes, channel, rate, offsets and transcript policy; cold-read the exact emitted samples and target.
- Core 15: treat unexpected sample-rate or channel changes as incidents. Restore original audio, annotations, preprocessing and consumer together.

## Exercises and worked answers

1. How long is [2,6) at 8 Hz? (6−2)/8=0.5 seconds, four samples.
2. What is wrong with calling the same bytes “16 Hz conversion”? The header changes their time meaning without computing a resampled signal.
3. A reference has two words and the hypothesis adds three extra words with no substitutions/deletions. What is WER? 3/2=150%; WER can exceed 100%.
4. Does a diarization cluster number identify a person? No. It is a clustering label under an algorithm/protocol; do not infer sensitive identities from it.

Acceptance: a reviewer must locate every target in original source time and reproduce the sample count. Recognition, generation and transcript normalization need separate gates.

Audio has at least three identities: the original recording, the selected time interval, and the canonical waveform emitted for training. Transcripts and speaker labels attach to specific intervals. Changing a boundary can change the correct target even if the filename remains the same.


## Distinguish the stages

Voice activity detection estimates where speech occurs. Diarization estimates who speaks when, usually as anonymous speaker clusters. ASR proposes words. Forced alignment places supplied words or phonemes in time. Source separation estimates component signals. These stages can assist each other, but none proves the others correct.

The pyannote.audio 2.1 paper describes local speaker segmentation, speaker embeddings, and global clustering. It explicitly notes that local speaker indices are not automatically consistent across windows. This is a useful warning for dataset production: a local cluster label is not a verified person identity, and merging segments requires evidence and review appropriate to the task. [R33]

WhisperX combines VAD-based cut/merge, batched transcription, and phoneme alignment. Its paper states that alignment models must suit the language and that a translated transcript lacks the direct phonetic correspondence needed for this alignment method. This separates three useful outputs: a transcript, its timing, and a translation. They should not be stored as interchangeable labels. [R34]



## Segment with the target in mind

Keep original start/end times and the exact transformation to exported samples. Check boundary rounding, channel selection, resampling, silence trimming, and duration. A transcript copied from an entire recording is not valid for every segment cut from it.

Avoid cutting words or discarding a quiet speaker through an aggressive VAD threshold. A low-energy segment may be valid whispered speech, while a loud segment may be music or clipping. Automatic quality scores should be calibrated against the intended corpus, including languages, accents, channel conditions, and speaking styles that matter.

Listen after conversion, not only before it. A file can satisfy the required WAV header while containing clipped, misordered, empty, or otherwise incorrect audio. Retain source and canonical hashes and rate/channel metadata. Normalization can be useful for one task but destroy amplitude information needed by another, so make it a recipe decision rather than a silent import default.

## Decide what the transcript represents

A verbatim transcript may preserve disfluencies, repetitions, and partial words. A normalized transcript may standardize numbers, punctuation, casing, and hesitations. Both can be legitimate targets, but mixing conventions without a rule creates avoidable disagreement.

Word error rate is (substitutions + deletions + insertions) divided by the number of reference words. It can exceed 100 percent when insertions are numerous. Character error rate uses characters instead. Both depend on tokenization and normalization. Report those choices, and examine names, numbers, technical terms, and other consequential units separately when aggregate error obscures them.

Timing quality is another axis. A transcript can be textually correct but shifted by several seconds; a forced aligner can assign plausible timestamps to wrong text. Review suspicious boundaries, competing hypotheses, and no-speech segments. Hallucinated text over silence is a distinct failure mode, not merely an ordinary substitution.

For diarization, record whether overlap is allowed, how unknown speakers are represented, and whether speaker count is supplied or inferred. Evaluate missed speech, false speech, and speaker confusion under a declared scoring convention. A good transcript with wrong speaker attribution can still be unusable for a dialogue task.

## Diversity and split design need more than speaker count

Speaker diversity, session diversity, linguistic diversity, and content diversity are different. Ten people reading the same ten sentences can support some speaker comparisons while providing narrow lexical coverage. One person recorded on many devices cannot establish unseen-speaker performance.

Choose the claim and design collection accordingly. If both unseen speakers and unseen scripts are required, a corpus in which every speaker reads every script can create a large connected family under both constraints. The solution may be a different collection design, not a cleverer random split. Do not mark every shared word or language as a protected group; protect relationships that would invalidate the stated claim.

Use consented, relevant metadata for coverage analysis rather than inferring sensitive identities from voices. Preserve permission for the actual use. Recognition training, redistribution, external transcription, and cloning an identifiable voice are different scopes. A public audio URL or a clean recording is not itself proof of all those permissions.

## Recognition and generation need distinct release gates

For recognition, the target is usually text or structured linguistic information conditioned on audio. For speech generation, audio is an output conditioned on text, speaker/style information, or other controls. For sound generation, the conditioning may be a class or caption rather than a transcript.

Speech-generation review should include content fidelity, pronunciation, artifacts, speaker consistency where authorized, prosody, and naturalness. Listening preferences and automatic acoustic metrics measure different properties. A high predicted quality score cannot establish that the intended words were spoken or that a voice use is permitted.

Retain the model-specific representation as a derivative: waveform, spectrogram, codec tokens, or other features. Pin preprocessing and verify that it matches the consumer. The tiny class-conditioned waveform example in the training companion is intentionally narrow and should not be presented as a universal speech-generation contract.

## Read the applicable subset terms

Emilia-Pipe is a useful methods reference for source separation, VAD, diarization, ASR, and quality assessment. Its repository acknowledges issues including overlap and hallucinated transcripts. The edition's cited card distinguishes noncommercial Emilia from CC-BY Emilia-YODAS despite a CC-BY-4.0 header. This is historical evidence of why subset terms matter, not a current access or license clearance. Recheck the exact acquired revision and applicable subset terms before use. [R35] [R36]

## Optional tools

No recorder or playback tool is needed for the paper interval. Later, an audio inspector, forced aligner and diarization tool can implement different stages; independently check interval and label quality. The Granary case below shows how segmentation, retranscription and filtering can change together.
