import React, { useState, useEffect } from 'react';
import { Stack } from 'expo-router';
import { View, Text, ScrollView } from 'react-native';
import { Container } from '~/components/Container';
import { ScreenContent } from '~/components/ScreenContent';
import * as epubjs from 'epubjs';

export default function Home() {
  const [epubContent, setEpubContent] = useState('');

  useEffect(() => {
    const loadEpub = async () => {
      try {
        // Load the EPUB file
        const response = await fetch('/assets/book.epub');
        const arrayBuffer = await response.arrayBuffer();
        
        // Create a new Book
        const book = epubjs.Book(arrayBuffer);
        
        // Generate the content
        let content = '';
        const spine = await book.loaded.spine;
        for (let item of spine.items) {
          const chapter = await item.load();
          content += chapter.document.body.innerHTML;
        }
        
        setEpubContent(content);
      } catch (error) {
        console.error('Error loading EPUB:', error);
      }
    };

    loadEpub();
  }, []);

  return (
    <>
      <Stack.Screen options={{ title: 'EPUB Reader' }} />
      <Container>
        <ScrollView style={{ flex: 1 }}>
          <Text>{epubContent}</Text>
        </ScrollView>
        <ScreenContent path="app/(drawer)/index.tsx" title="EPUB Reader" />
      </Container>
    </>
  );
}
