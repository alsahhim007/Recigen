<template>
    <v-container>
        <v-container>
            <v-row justify="center">
                <v-col cols="auto">
                    <v-btn @click="isText = true" height="50" min-width="130">
                        Search with Text
                    </v-btn>
                </v-col>

                <v-col cols="auto">
                    <v-btn @click="isText = false" height="50" min-width="130">
                        Search with Image
                    </v-btn>
                </v-col>
            </v-row>
        </v-container>
        <v-card class="mx-auto mt-10" color="grey-lighten-3" max-width="400">
            <v-card-text v-show="isText">
                <v-text-field v-model="textInput" label="Search for Recipe" outlined></v-text-field>
            </v-card-text>

            <v-card-text v-show="!isText">
                <v-file-input v-model="selectedFile" label="Choose an image" show-size accept="image/*"></v-file-input>
            </v-card-text>
        </v-card>
        <v-container>
            <v-row justify="center">
                <v-col cols="auto">
                    <v-btn @click="postRequest()" height="50" min-width="130">
                        Search
                    </v-btn>
                </v-col>
            </v-row>
        </v-container>
        <v-card class="mx-auto" max-width="1344">
            <v-card-text v-show="isMessage">
                <p v-html="noMessage.Message"></p>
            </v-card-text>
            <v-container fluid v-show="isCards">
                <v-row dense>
                    <v-col v-for="card, index in cards" :key="card.title" cols="4">
                        <v-card>
                            <v-img :src="card.src" class="align-end" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                                height="200px" cover>
                                <v-card-title class="text-white" v-text="card.title"></v-card-title>
                                <v-card-subtitle></v-card-subtitle>
                            </v-img>
                            <v-card-actions>
                                <v-btn variant="text" color="teal-accent-4" @click="toggleDetails(index)">
                                    Details
                                </v-btn>
                            </v-card-actions>
                            <v-expand-transition v-if="reveal[index]">
                                <v-card class="v-card--reveal" style="height: 100%;">
                                    <v-card-text class="pb-0">
                                        <p class="text-h4 text--primary">
                                            Instructions
                                        </p>
                                        <p v-html="card.instuctions"></p>
                                    </v-card-text>
                                </v-card>
                            </v-expand-transition>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-card>
    </v-container>
</template>

<script>

export default {

    data: () => ({
        isText: true,
        textInput: '',
        response: '',
        cards: [],
        noMessage: {},
        isCards: false,
        reveal: [],
        isMessage: false,
        selectedFile: null,
    }),
    methods: {
        async postRequest() {
            try {
                let formData = new FormData();
                formData.append('image', this.selectedFile);
                this.cards = [];
                this.isMessage = false;
                let url_params = {}
                if (this.selectedFile) {
                    console.log(this.selectedFile)
                    url_params = {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        },
                        body: this.selectedFile
                    }
                }
                else {
                    url_params = {
                        method: 'POST',
                        body: JSON.stringify({ search: this.textInput })
                    }
                }
                await fetch('https://pozo3x3fwl.execute-api.us-east-1.amazonaws.com/prod/searchrecipe', url_params);
                await fetch('https://2hpy5cq00l.execute-api.us-east-1.amazonaws.com/prod/poll', {
                    method: 'POST',
                    body: JSON.stringify({})
                }).then(response => response.json())
                    .then(data => {
                        data = JSON.parse(JSON.stringify(data));
                        if ('Message' in data) {
                            this.noMessage['Message'] = data['Message']
                        } else {
                            let data_body = data['body'];
                            if (Object.keys(data_body).length === 0) {
                                this.noMessage['Message'] = "No recipe found with given items"
                                this.isMessage = true;
                            } else {
                                this.noMessage = {}
                                for (let i = 0; i < Object.keys(data_body).length; i++) {
                                    this.cards[i] = data_body[i.toString()];
                                }
                                this.reveal = Array(this.cards.length).fill(false);
                                this.isCards = true;
                            }
                        }
                    });
            } catch (error) {
                console.error(error);
            }
        },
        toggleDetails(index) {
            this.$set(this.reveal, index, !this.reveal[index]);
        }
    }
}
</script>